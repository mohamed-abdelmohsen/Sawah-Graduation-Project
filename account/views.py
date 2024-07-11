from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.conf import settings
from .models import Profile
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('dashboard')
            else:
                # Invalid login
                messages.error(request,"Wrong Username Or Password")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            Profile.objects.create(user=new_user, date_of_birth=None, photo=None)

            # Welcome email
            subject = "Welcome to SAWAH - sawah admin"
            message = f"Hello, {user_form.cleaned_data['first_name']}.\nThanks for visiting our website.\n We hope you good time.\n Sawah Team."
            from_email = settings.EMAIL_HOST_USER
            to_list = [user_form.cleaned_data['email']]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email address configuration email
            current_site = get_current_site(request)
            email_subject = "Confirm your email"
            message2 = render_to_string('account/email_configration.html', {
                'name': user_form.cleaned_data['first_name'],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': generate_token.make_token(new_user),
            })

            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                to=[user_form.cleaned_data['email']],
            )
            email.send(fail_silently=True)

            return render(request, 'registration/login.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile Updated Successfully!")
        else:
            messages.error(request, "Error Updating Your Profile!")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('sawah:home')

    else:
        return render(request, 'account/activation_failed.html')
    
    

from django.views.generic import View
from django.http import HttpResponse

class TwitterAuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        # Handle Twitter authentication callback here
        # This is where you can access the authenticated user's data
        return HttpResponse("Twitter authentication callback handled successfully")

from sawah.models import *
from sawah.views import calculate_landmark_rating, calculate_hotel_rating, calculate_restaurant_rating

@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'account/profile.html', {'user':user})


@login_required
def liked_places_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    content_type_id = ContentType.objects.get_for_model(Landmark).id
    favorite_landmarks_ids = Favorite.objects.filter(
        user=user, 
        content_type_id=content_type_id
    ).values_list('object_id', flat=True)
    favorite_landmarks = Landmark.objects.filter(id__in=favorite_landmarks_ids)

    favorite_landmarks_with_ratings = [
        (landmark, calculate_landmark_rating(landmark)) for landmark in favorite_landmarks
    ]

    context = {
        'user': user,
        'favorite_landmarks_with_ratings': favorite_landmarks_with_ratings,
    }
    
    return render(request, 'account/liked_places.html', context)

@login_required
def liked_hotels_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    content_type_id = ContentType.objects.get_for_model(Hotel).id
    favorite_hotels_ids = Favorite.objects.filter(
        user=user, 
        content_type_id=content_type_id
    ).values_list('object_id', flat=True)
    favorite_hotels = Hotel.objects.filter(id__in=favorite_hotels_ids)

    favorite_hotels_with_ratings = [
        (landmark, calculate_hotel_rating(landmark)) for landmark in favorite_hotels
    ]

    context = {
        'user': user,
        'favorite_hotels_with_ratings': favorite_hotels_with_ratings,
    }
    
    return render(request, 'account/liked_hotels.html', context)

@login_required
def liked_restaurants_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    content_type_id = ContentType.objects.get_for_model(Restaurant).id
    favorite_restaurants_ids = Favorite.objects.filter(
        user=user, 
        content_type_id=content_type_id
    ).values_list('object_id', flat=True)
    favorite_restaurants = Restaurant.objects.filter(id__in=favorite_restaurants_ids)

    favorite_restaurants_with_ratings = [
        (restaurant, calculate_restaurant_rating(restaurant)) for restaurant in favorite_restaurants
    ]

    context = {
        'user': user,
        'favorite_restaurants_with_ratings': favorite_restaurants_with_ratings,
    }
    
    return render(request, 'account/liked_restaurants.html', context)

from sawah.models import HotelComment, RestaurantComment, LandmarkComment

def hotel_comments(request,user_id):
    user = get_object_or_404(User, id=user_id)
    hotel_comment = HotelComment.objects.filter(user=user)
    return render(request,'account/profile_hotel_comments.html',{'user':user,'hotel_comment':hotel_comment})

def restuarant_comments(request,user_id):
    user = get_object_or_404(User, id=user_id)
    restaurant_comment = RestaurantComment.objects.filter(user=user)
    return render(request,'account/profile_rest_comments.html',{'user':user,'restaurant_comment':restaurant_comment})

def landmark_comments(request,user_id):
    user = get_object_or_404(User, id=user_id)
    landmark_comment = LandmarkComment.objects.filter(user=user)
    return render(request,'account/profile_land_comments.html',{'user':user,'landmark_comment':landmark_comment})