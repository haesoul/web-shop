from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import *
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    template_name = 'users/register_view.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')



class MyLoginView(LoginView):
    model = CustomUser
    template_name = 'users/login_view.html'
    form_class = AuthenticationForm
    next_page = 'home'
    success_url = reverse_lazy('home')

    redirect_authenticated_user = True


# class MyLogoutView(LogoutView):
#     model = CustomUser
#     template_name = 'user/login_view.html'
#     form_class = RegisterUserForm