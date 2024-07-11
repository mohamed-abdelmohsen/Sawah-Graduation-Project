from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import RestaurantCommentForm, HotelCommentForm, LandmarkCommentForm, SearchForm
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Restaurant, Landmark, HotelRating,\
HotelComment, RestaurantComment, LandmarkComment,LandmarkRating, RestaurantRating,\
    City,Favorite, Events
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import IntegrityError
import requests
from django.http import JsonResponse, HttpResponseBadRequest
import base64
from .filter import HotelFilter, LandmarkFilter, RestaurantFilter



def home(request):
    search_form = SearchForm()
    top_rated_hotels = Hotel.objects.annotate(avg_rating=Avg('hotel_rating__stars')).order_by('-avg_rating')[:12]
    top_rated_landmarks = Landmark.objects.annotate(avg_rating=Avg('landmark_rating__stars')).order_by('-avg_rating')[:12]
    top_rated_restaurants = Restaurant.objects.annotate(avg_rating=Avg('restaurant_rating__stars')).order_by('-avg_rating')[:12]
    events = Events.objects.all()
    cities = City.objects.all()

    return render(request, 'sawah/home.html',{'top_rated_hotels':top_rated_hotels,
                                              'search_form':search_form,
                                              'top_rated_landmarks':top_rated_landmarks,
                                              'top_rated_restaurants':top_rated_restaurants,
                                              'events':events,
                                              'cities':cities
                                              })


def calculate_hotel_rating(hotel):
    return HotelRating.objects.filter(hotel=hotel).aggregate(Avg('stars'))['stars__avg']


def calculate_restaurant_rating(restaurant):
    return RestaurantRating.objects.filter(restaurant=restaurant).aggregate(Avg('stars'))['stars__avg']


def calculate_landmark_rating(landmark):
    return LandmarkRating.objects.filter(landmark=landmark).aggregate(Avg('stars'))['stars__avg']


def city_list(request):
    city = City.objects.all()
    return render(request, 'sawah/city_list.html', {'city':city})

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    hotels = Hotel.objects.filter(city=city).annotate(avg_rating=Avg('hotel_rating__stars')).order_by('-avg_rating')
    landmarks = Landmark.objects.filter(city=city).annotate(avg_rating=Avg('landmark_rating__stars')).order_by('-avg_rating')
    restaurants = Restaurant.objects.filter(city=city).annotate(avg_rating=Avg('restaurant_rating__stars')).order_by('-avg_rating')
    top_rated_landmarks = Landmark.objects.filter(city=city).annotate(avg_rating=Avg('landmark_rating__stars')).order_by('-avg_rating')[:12]
    events = Events.objects.all()

    return render(request, 'sawah/city_detail.html',{'city':city,'hotels':hotels, 'landmarks':landmarks,
                                                     'restaurants':restaurants, 'top_rated_landmarks':top_rated_landmarks,
                                                     'events':events
                                                     })


def city_hotels(request, city_id):
    city = get_object_or_404(City, id=city_id)
    filter = HotelFilter(request.GET, queryset=Hotel.objects.filter(city=city))
    hotels = filter.qs
    for hotel in hotels:
        hotel.comments = calculate_hotel_comments(hotel)
        hotel.ratings = calculate_hotel_rating(hotel)
    
    return render(request, 'sawah/city_hotels.html', {'filter':filter, 'hotels': hotels, 'city':city})

def city_landmarks(request, city_id):
    city = get_object_or_404(City, id=city_id)
    filter = LandmarkFilter(request.GET, queryset=Landmark.objects.filter(city=city))
    landmarks = filter.qs
    for landmark in landmarks:
        landmark.comments = calculate_landmark_comments(landmark)
        landmark.ratings = calculate_landmark_rating(landmark)
    
    return render(request, 'sawah/city_landmarks.html', {'filter':filter, 'landmarks': landmarks, 'city':city})

def city_restaurants(request, city_id):
    city = get_object_or_404(City, id=city_id)
    filter = RestaurantFilter(request.GET, queryset=Restaurant.objects.filter(city=city))
    restaurants = filter.qs
    for restaurant in restaurants:
        restaurant.comments = calculate_restaurant_comments(restaurant)
        restaurant.ratings = calculate_restaurant_rating(restaurant)
    
    return render(request, 'sawah/city_restaurants.html', {'filter':filter, 'restaurants': restaurants, 'city':city})



def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel_ratings = calculate_hotel_rating(hotel)
    comments = hotel.hotel_comments.filter(active=True)
    content_type_id = ContentType.objects.get_for_model(Hotel).id

    # Check if the hotel is in the user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, content_type_id=content_type_id, object_id=hotel_id).exists()

    form = HotelCommentForm()
    return render(request, 'sawah/hotel_details.html', {
        'hotel': hotel,
        'comments': comments,
        'form': form,
        'hotel_ratings': hotel_ratings,
        'item_content_type_id': content_type_id,
        'object_id': hotel_id,
        'is_favorite': is_favorite
    })


@login_required
def hotel_comment(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    user = request.user
    
    try:
        user_rating = HotelRating.objects.get(user=user, hotel=hotel)
    except HotelRating.DoesNotExist:
        user_rating = None
    
    if request.method == 'POST':
        form = HotelCommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.hotel = hotel
            comment.user = user
            comment.save()
            
            if user_rating:
                user_rating.stars = form.cleaned_data['rating']
                user_rating.save()
            else:
                try:
                    user_rating = HotelRating.objects.create(user=user, hotel=hotel, stars=form.cleaned_data['rating'])
                except IntegrityError:
                    pass
            
            return redirect('sawah:hotel_detail', hotel_id=hotel_id)   
    else:
        initial_rating = user_rating.stars if user_rating else None
        form = HotelCommentForm(initial={'rating': initial_rating})

    return render(request, 'sawah/hotel_comment.html', {
        'hotel': hotel,
        'form': form
    })


    
    
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    comments = restaurant.restaurants_comments.filter(active=True)
    restaurant_rating = calculate_restaurant_rating(restaurant)
    content_type_id = ContentType.objects.get_for_model(Restaurant).id

    # Check if the restaurant is in the user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, content_type_id=content_type_id, object_id=restaurant_id).exists()

    form = RestaurantCommentForm()
    return render(request, 'sawah/restaurant_details.html', {
        'restaurant': restaurant,
        'comments': comments,
        'form': form,
        'restaurant_rating': restaurant_rating,
        'item_content_type_id': content_type_id,
        'object_id': restaurant_id,
        'is_favorite': is_favorite
    })

@login_required
def restaurant_comment(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user = request.user
    comment = None
    user_rating = None
    
    try:
        user_rating = RestaurantRating.objects.get(user=user, restaurant=restaurant)
    except RestaurantRating.DoesNotExist:
        user_rating = None
    
    if request.method == 'POST':
        form = RestaurantCommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            comment.user = user
            comment.save()
            if user_rating:
                user_rating.stars = form.cleaned_data['rating']
                user_rating.save()
            else:
                try:
                    user_rating = RestaurantRating.objects.create(user=user, restaurant=restaurant, stars=form.cleaned_data['rating'])
                except IntegrityError:
                    pass
            
            return redirect('sawah:restaurant_detail', restaurant_id=restaurant_id)
    else:
        form = RestaurantCommentForm()

    return render(request, 'sawah/restaurant_comment.html', {
        'restaurant': restaurant,
        'comment': comment,
        'form': form
    })




def landmark_detail(request, landmark_id):
    landmark = get_object_or_404(Landmark, id=landmark_id)
    comments = landmark.landmark_comments.filter(active=True)
    landmark_rating = calculate_landmark_rating(landmark)
    content_type = ContentType.objects.get_for_model(Landmark)
    content_type_id = content_type.id

    # Check if the landmark is in the user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, content_type_id=content_type_id, object_id=landmark_id).exists()

    form = LandmarkCommentForm()
    
    context = {
        'landmark': landmark,
        'comments': comments,
        'form': form,
        'landmark_rating': landmark_rating,
        'is_favorite': is_favorite,
        'item_content_type_id': content_type_id,
        'object_id': landmark_id
    }

    return render(request, 'sawah/landmark_details.html', context)


@login_required
def landmark_comment(request, landmark_id):
    landmark = get_object_or_404(Landmark, id=landmark_id)
    user = request.user
    comment = None
    user_rating = None
    
    try:
        user_rating = LandmarkRating.objects.get(user=user, landmark=landmark)
    except LandmarkRating.DoesNotExist:
        user_rating = None
    
    if request.method == 'POST':
        form = LandmarkCommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.landmark = landmark
            comment.user = user
            comment.save()
            
            # Create or update LandmarkRating
            if user_rating:
                user_rating.stars = form.cleaned_data['rating']
                user_rating.save()
            else:
                try:
                    user_rating = LandmarkRating.objects.create(user=user, landmark=landmark, stars=form.cleaned_data['rating'])
                except IntegrityError:
                    # Handle IntegrityError (e.g., log the error, notify user, etc.)
                    pass
            
            return redirect('sawah:landmark_detail', landmark_id=landmark_id)
    else:
        form = LandmarkCommentForm()  # Use LandmarkCommentForm for GET requests too

    return render(request, 'sawah/landmark_comment.html', {
        'landmark': landmark,
        'comment': comment,
        'form': form
    })



def top_rated_hotels(request):
    top_rated_hotels = Hotel.objects.annotate(avg_rating=Avg('hotel_rating__stars')).order_by('-avg_rating')[:5]
    context = {'top_rated_hotels':top_rated_hotels}
    return render(request, 'sawah/includes/top_rated_hotels.html',context)


def calculate_hotel_comments(hotel):
    return HotelComment.objects.filter(hotel=hotel).count()

def calculate_restaurant_comments(restaurant):
    return RestaurantComment.objects.filter(restaurant=restaurant).count()

def calculate_landmark_comments(landmark):
    return LandmarkComment.objects.filter(landmark=landmark).count()


def search_view(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            hotel_results = Hotel.objects.annotate(
                search = SearchVector('name','description'),
            ).filter(search__icontains = query)
            
            for hotel in hotel_results:
                hotel.rating = calculate_hotel_rating(hotel)
                hotel.comments = calculate_hotel_comments(hotel)
                results.append(hotel)
            
            restaurant_results = Restaurant.objects.filter(
                Q(name__icontains = query) | Q(description__icontains = query) 
            )
            for restaurant in restaurant_results:
                restaurant.rating = calculate_restaurant_rating(restaurant)
                restaurant.comments = calculate_restaurant_comments(restaurant)
                results.append(restaurant)
            
            landmark_results = Landmark.objects.filter(
                Q(name__icontains = query) | Q(description__icontains = query) 
            )
            for landmark in landmark_results:
                landmark.rating = calculate_landmark_rating(landmark)
                landmark.comments = calculate_landmark_comments(landmark)
                results.append(landmark)
            results = list(hotel_results) + list(restaurant_results) +list(landmark_results)
            
    return render(request, 'sawah/search.html', {'form':form, 'query':query, 'results':results})           


@login_required
def add_to_favorites(request, content_type_id, object_id):
    if request.user.is_authenticated:
        content_type = ContentType.objects.get_for_id(content_type_id)
        item = content_type.get_object_for_this_type(pk=object_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, content_type=content_type, object_id=object_id)
        if not created:
            pass
    return redirect(item.get_absolute_url())

@login_required
def remove_from_favorites(request, content_type_id, object_id):
    if request.user.is_authenticated:
        content_type = ContentType.objects.get_for_id(content_type_id)
        item = content_type.get_object_for_this_type(pk=object_id)
        Favorite.objects.filter(user=request.user, content_type_id=content_type_id, object_id=object_id).delete()
    return redirect(item.get_absolute_url())



def scan_face_view(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
        else:
            return HttpResponseBadRequest('Image file not provided')

        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        api_url = "https://ec72-197-35-195-41.ngrok-free.app/scan_face"
        try:
            response = requests.post(api_url, json=encoded_image)

            print(f"API Response Status Code: {response.status_code}")
            print(f"API Response JSON: {response.json()}")

            if response.status_code == 200:
                data = response.json()
                video_path = data.get('video_path', None)
                if video_path:
                    print(f"Redirect URL: {video_path}")
                    video_url = request.build_absolute_uri(settings.MEDIA_URL + video_path)
                    
                    return JsonResponse({'status': 'success', 'redirect_url': video_url})
                else:
                    return render(request, 'sawah/capture_image.html', {'error_message': 'Video path not found'})
            else:
                return render(request, 'sawah/capture_image.html', {'error_message': 'API request failed'})

        except requests.exceptions.RequestException as e:
            return render(request, 'sawah/capture_image.html', {'error_message': str(e)})

    return render(request, 'sawah/capture_image.html')


def scan_result_view(request):
    video_url = request.GET.get('video_url', '')
    return render(request, 'sawah/scan_result.html', {'video_url': video_url})



def hotels_view(request):
    filter = HotelFilter(request.GET, queryset=Hotel.objects.all())
    hotels = filter.qs
    for hotel in hotels:
        hotel.ratings = calculate_hotel_rating(hotel)
        hotel.comments = calculate_hotel_comments(hotel)
    return render(request, 'sawah/Egypt_hotels.html',{'filter':filter, 'hotels': hotels})


def landmarks_view(request):
    filter = LandmarkFilter(request.GET, queryset=Landmark.objects.all())
    landmarks = filter.qs
    for landmark in landmarks:
        landmark.ratings = calculate_landmark_rating(landmark)
        landmark.comments = calculate_landmark_comments(landmark)
    return render(request, 'sawah/Egypt_landmarks.html',{'filter':filter, 'landmarks': landmarks})

def restaurants_view(request):
    filter = RestaurantFilter(request.GET, queryset=Restaurant.objects.all())
    restaurants = filter.qs
    for restaurant in restaurants:
        restaurant.ratings = calculate_restaurant_rating(restaurant)
        restaurant.comments = calculate_restaurant_comments(restaurant)
    return render(request, 'sawah/Egypt_restaurants.html',{'filter':filter, 'restaurants': restaurants})