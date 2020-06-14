from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,)
    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2', )
