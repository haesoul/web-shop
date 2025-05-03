from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="",
        error_messages={
            'required': "Пожалуйста, укажите имя пользователя.",
            'max_length': "Имя слишком длинное (не более 150 символов).",
            'invalid': "Можно использовать только буквы, цифры и @/./+/-/_."
        }
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Введите пароль!",
            'min_length': "Пароль должен быть не короче 6 символов!",
        }
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Повторите пароль!",
        }
    )
    class Meta:
        model = CustomUser

        fields = ['username','photo','location']



class LoginUser(forms.ModelForm):
    class Meta:
        model = CustomUser

        fields = ['username','password']












