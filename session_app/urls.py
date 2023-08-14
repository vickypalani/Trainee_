from django.urls import path
from . import views

app_name = "session_app"

urlpatterns = [
    path("", views.DashBoardView.as_view(), name="dashboard"),
    path("random", views.Random.as_view(), name="logout"),

]
