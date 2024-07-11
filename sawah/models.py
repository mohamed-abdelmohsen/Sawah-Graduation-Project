from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class City(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sawah:city_detail', kwargs={'city_id':self.pk})


class CityImageModel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

class Place(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.CharField(_('slug'), max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(_('available'), default=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]
        abstract = True

    def __str__(self):
        return self.name


class Hotel(Place):
    def get_absolute_url(self):
        return reverse('sawah:hotel_detail', kwargs={'hotel_id': self.pk})


class Landmark(Place):
    def get_absolute_url(self):
        return reverse('sawah:landmark_detail', kwargs={'landmark_id': self.pk})


class Restaurant(Place):
    def get_absolute_url(self):
        return reverse('sawah:restaurant_detail', kwargs={'restaurant_id': self.pk})


class HotelRating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    objects = models.Manager()     # unresolved
    
    class Meta:
        unique_together = ('user', 'hotel')
        index_together = ('user', 'hotel')


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('user', 'restaurant')
        index_together = ('user', 'restaurant')
        
        
class LandmarkRating(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('user', 'landmark')
        index_together = ('user', 'landmark')

        
class Comment(models.Model):
    TRAVEL_WITH_CHOICES = [
        ('family', 'Family'),
        ('partner', 'Partner'),
        ('work', 'Work'),
        ('friends', 'Friends'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    story = models.CharField(max_length=200, blank=True, null=True)
    travel_with = models.CharField(max_length=10, choices=TRAVEL_WITH_CHOICES, blank=True, null=True)
    travel_date = models.DateField(blank=True, null=True)
    best_time_choices = [
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('spring', 'Spring'),
        ('autumn', 'Autumn'),
    ]
    best_time = models.CharField(max_length=10, choices=best_time_choices, blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        abstract = True

    indexes = [
        models.Index(fields=['created']),
    ]


class HotelComment(Comment):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_comments')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.rating is not None:
            hotel_rating, created = HotelRating.objects.update_or_create(
                hotel=self.hotel,
                user=self.user,
                defaults={'stars': self.rating}
            )
            if not created:
                hotel_rating.stars = self.rating
                hotel_rating.save()

    def __str__(self):
        return f'Comment by {self.user} on {self.hotel}'


class RestaurantComment(Comment):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurants_comments')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.rating is not None:
            restaurant_rating, created = RestaurantRating.objects.get_or_create(
                restaurant=self.restaurant,
                user=self.user,
                defaults={'stars': self.rating}
            )
            if not created:
                restaurant_rating.stars = self.rating
                restaurant_rating.save()

    def __str__(self):
        return f'Comment by {self.user} on {self.restaurant}'


class LandmarkComment(Comment):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_comments')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.rating is not None:
            landmark_rating, created = LandmarkRating.objects.get_or_create(
                landmark=self.landmark,
                user=self.user,
                defaults={'stars': self.rating}
            )
            if not created:
                landmark_rating.stars = self.rating
                landmark_rating.save()

    def __str__(self):
        return f'Comment by {self.user} on {self.landmark}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Events(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    date = models.DateField()




