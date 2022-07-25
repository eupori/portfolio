from django import forms
from django.contrib.auth.forms import UserCreationForm

from mysite.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
