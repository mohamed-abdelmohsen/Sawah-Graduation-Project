from django.urls import path
from . import views

app_name = 'sawah'

urlpatterns=[
    path('home/',views.home,name='home'),
    path('city/', views.city_list, name='city_list'),
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('hotels/', views.hotels_view, name='hotels'),
    path('landmarks/', views.landmarks_view, name='landmarks'),
    path('restaurants/', views.restaurants_view, name='restaurants'),
    path('city/<int:city_id>/hotels/', views.city_hotels, name='city_hotels'),
    path('city/<int:city_id>/landmarks/', views.city_landmarks, name='city_landmarks'),
    path('city/<int:city_id>/restaurants/', views.city_restaurants, name='city_restaurants'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/<int:hotel_id>/comment/',views.hotel_comment, name='hotel_comment'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:restaurant_id>/comment/',views.restaurant_comment, name='restaurant_comment'),
    path('landmarks/<int:landmark_id>/', views.landmark_detail, name='landmark_detail'),
    path('landmarks/<int:landmark_id>/comment/', views.landmark_comment, name='landmark_comment'),
    path('top-rated-hotels/', views.top_rated_hotels, name='top_rated_hotels'),
    path('search/', views.search_view, name='search'),
    path('add_to_favorites/<int:content_type_id>/<int:object_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:content_type_id>/<int:object_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('scan_face_view/', views.scan_face_view, name='scan_face_view'),
    path('scan_result/', views.scan_result_view, name='scan_result_view'),



]
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)