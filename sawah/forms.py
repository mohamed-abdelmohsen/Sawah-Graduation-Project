from django import forms
from .models import *

from django import forms
from .models import HotelComment

class HotelCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['travel_with'].choices = [(choice[0], choice[1]) for choice in self.fields['travel_with'].choices if choice[0] != '']
        self.fields['best_time'].choices = [(choice[0], choice[1]) for choice in self.fields['best_time'].choices if choice[0] != '']

    class Meta:
        model = HotelComment
        fields = ['body', 'story', 'rating', 'travel_with', 'travel_date', 'best_time', 'advice']
        widgets = {
            'body': forms.TextInput(attrs={'class': 'in','placeholder':'Describe your trip in one statement'}),
            'story': forms.TextInput(attrs={'class': 'in','placeholder':'Tell us your story'}),
            'travel_with': forms.RadioSelect(attrs={'class': 'tt'}),
            'travel_date': forms.DateInput(attrs={'class': 'BR', 'type': 'date'}),
            'best_time': forms.RadioSelect(attrs={'class': 'tt'}),
            'advice': forms.TextInput(attrs={'class': 'in', 'placeholder':'Do you have any advice to make this trip more better?'}),
        }

            
        
class LandmarkCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['travel_with'].choices = [(choice[0], choice[1]) for choice in self.fields['travel_with'].choices if choice[0] != '']
        self.fields['best_time'].choices = [(choice[0], choice[1]) for choice in self.fields['best_time'].choices if choice[0] != '']

    class Meta:
        model = LandmarkComment
        fields = ['body', 'story', 'rating', 'travel_with', 'travel_date', 'best_time', 'advice']
        widgets = {
            'body': forms.TextInput(attrs={'class': 'in','placeholder':'Describe your trip in one statement'}),
            'story': forms.TextInput(attrs={'class': 'in','placeholder':'Tell us your story'}),
            'travel_with': forms.RadioSelect(attrs={'class': 'tt'}),
            'travel_date': forms.DateInput(attrs={'class': 'BR', 'type': 'date'}),
            'best_time': forms.RadioSelect(attrs={'class': 'tt'}),
            'advice': forms.TextInput(attrs={'class': 'in', 'placeholder':'Do you have any advice to make this trip more better?'}),
        }


class RestaurantCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['travel_with'].choices = [(choice[0], choice[1]) for choice in self.fields['travel_with'].choices if choice[0] != '']
        self.fields['best_time'].choices = [(choice[0], choice[1]) for choice in self.fields['best_time'].choices if choice[0] != '']

    class Meta:
        model = RestaurantComment
        fields = ['body', 'story', 'rating', 'travel_with', 'travel_date', 'best_time', 'advice']
        widgets = {
            'body': forms.TextInput(attrs={'class': 'in','placeholder':'Describe your trip in one statement'}),
            'story': forms.TextInput(attrs={'class': 'in','placeholder':'Tell us your story'}),
            'travel_with': forms.RadioSelect(attrs={'class': 'tt'}),
            'travel_date': forms.DateInput(attrs={'class': 'BR', 'type': 'date'}),
            'best_time': forms.RadioSelect(attrs={'class': 'tt'}),
            'advice': forms.TextInput(attrs={'class': 'in', 'placeholder':'Do you have any advice to make this trip more better?'}),
        }
        
#:) متنساش الوراثة لما تيجي تكمل يسطا


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = HotelRating
        fields = ['stars']
        widgets = {'stars': forms.NumberInput(attrs={'type': 'number', 'min': 1, 'max': 5})}


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search'}))