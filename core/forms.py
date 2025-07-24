from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(UserChangeForm):
    password = None  

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BookingForm(forms.Form):
    seats = forms.IntegerField(min_value=1, label='Number of Seats')
