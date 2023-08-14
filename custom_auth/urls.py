from django.urls import path
from . import views

app_name = "custom_auth"

urlpatterns = [
    path("registration", views.CustomSignUpView.as_view(), name="registration"),
    path("login", views.CustomSignInForm.as_view(), name="login"),
    path("logout", views.SignOut.as_view(), name="logout"),
]
