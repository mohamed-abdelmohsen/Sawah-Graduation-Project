from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ImageField, FileInput

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'email'
        ]
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match!")
        return cd['password2']
    

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already exists!')
        return data
    
    
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=['first_name','username','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'c','placeholder':'Your name', 'data-aos':'fade-up-right', 'data-aos-duration':'3000'}),
            'username': forms.TextInput(attrs={'class':'c', 'placeholder':'Username', 'data-aos':'fade-up-right', 'data-aos-duration':'3000'}),
            'email': forms.TextInput(attrs={'class':'c', 'placeholder':'Email', 'data-aos':'fade-up-right', 'data-aos-duration':'3000'}),

        }
        
    def clean_email(self):
        data=self.cleaned_data['email']
        qs=User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use!")
        return data
        

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'c',
        'placeholder': 'Date of birth',
        'type': 'date',
        'data-aos':'fade-up-right',
        'data-aos-duration':'3000'
    }))
    photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'c',
    }))

    
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']

    
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)