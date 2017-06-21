from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30)
