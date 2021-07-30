from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']




'''class ProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # previous_password = forms.PasswordInput()

    class Meta:
        model = Profile
        fields = ('email','username','profileImage')
'''
class Userupdateform(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):   
    class Meta:
        model = Profile
        fields = ['image','bio','buyer']
