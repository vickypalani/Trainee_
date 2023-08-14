from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm

# Create your views here.
class CustomSignUpView(FormView):
    template_name ='auth/registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy("custom_auth:login")


class CustomSignInForm(LoginView):
    template_name = 'auth/login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy("session_app:dashboard")


class SignOut(LogoutView):
    pass
