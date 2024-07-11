from django.urls import path,include
from . import views
from .views import TwitterAuthCallbackView



urlpatterns =[
    
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('',include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('social-auth/complete/twitter/', TwitterAuthCallbackView.as_view(), name='twitter_auth_callback'),
    path('profile/<int:user_id>',views.profile_view, name='profile'),
    path('<int:user_id>/liked_places/',views.liked_places_view, name='liked_places'),
    path('<int:user_id>/liked_hotels/',views.liked_hotels_view, name='liked_hotels'),
    path('<int:user_id>/liked_restaurants/',views.liked_restaurants_view, name='liked_restaurants'),
    path('profile/<int:user_id>/hotel_comments/', views.hotel_comments,name='hotels_comment'),
    path('profile/<int:user_id>/restaurant_comments/', views.restuarant_comments,name='restaurants_comment'),
    path('profile/<int:user_id>/landmark_comments/', views.landmark_comments,name='landmarks_comment'),


]
