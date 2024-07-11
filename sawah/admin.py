from django.contrib import admin
from .models import Hotel, Restaurant,Landmark, HotelComment, LandmarkComment, RestaurantComment, HotelRating,City\
    ,LandmarkRating, RestaurantRating, Favorite, Events, CityImageModel

class ImageModelInline(admin.TabularInline):
    model = CityImageModel
    extra = 3  

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ImageModelInline]










@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}




@admin.register(HotelComment)
class HotelCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user', 'body']
    
@admin.register(LandmarkComment)
class LandmarkCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'landmark', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user', 'body']
    
    
@admin.register(RestaurantComment)
class RestaurantCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user', 'body']
    
    
@admin.register(HotelRating)
class HotelRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'stars']
    list_filter = ['stars']
    
@admin.register(LandmarkRating)
class LandmarkRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'landmark', 'stars']
    list_filter = ['stars']
    
@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'stars']
    list_filter = ['stars']
    
@admin.register(Favorite)
class FavAdmin(admin.ModelAdmin):
        list_display = ['user', 'content_type']
        

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']