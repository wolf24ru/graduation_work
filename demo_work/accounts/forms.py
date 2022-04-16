from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    phone_number = forms.CharField(max_length=12)
    # id_permission = forms.

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')
