from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from blog.models import Article, Comment


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=30)
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    email = forms.EmailField(label="Почта")
    password1 = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
