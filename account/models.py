from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d')

    def __str__(self):
        return f'profile of {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user.id})
