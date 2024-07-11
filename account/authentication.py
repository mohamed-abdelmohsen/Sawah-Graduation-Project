from django.contrib.auth.models import User
from account.models import Profile


class EmailAuthBackend:
    
    def authenticate(slef,request,username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
    def get_user(self,user_id):
        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
from django.contrib.auth.models import User
from .models import Profile  # Import your Profile model

def create_profile(backend, user, response, *args, **kwargs):
    # Get or create the profile associated with the user
    profile, created = Profile.objects.get_or_create(user=user)

    # If the profile was just created, populate it with initial data
    if created:
        # Extract relevant information from the social provider's response
        if backend.name == 'facebook':
            # Example: Extract profile picture URL from Facebook response
            profile.picture_url = response.get('picture', {}).get('data', {}).get('url')

        # Save the profile with the initial data
        profile.save()

    # Return the profile
    return {'profile': profile}

    