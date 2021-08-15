from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname','birth_date','interestedin',)




