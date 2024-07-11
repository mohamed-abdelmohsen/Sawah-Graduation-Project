import django_filters
from .models import Hotel, Landmark, Restaurant

class HotelFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='hotel_rating__stars', lookup_expr='exact')

    class Meta:
        model = Hotel
        fields = ['name']


class LandmarkFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='landmark_rating__stars', lookup_expr='exact')

    class Meta:
        model = Landmark
        fields = ['name']

class RestaurantFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='restaurant_rating__stars', lookup_expr='exact')

    class Meta:
        model = Restaurant
        fields = ['name']