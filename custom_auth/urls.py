from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy

app_name = "custom_auth"

urlpatterns = [
    path("registration", views.customSignupPage, name="registration"),
    path("login", views.customSiginPage, name="login"),
    path("logout", views.SignOut.as_view(), name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name='auth/password_reset.html', email_template_name = 'auth/password_reset_email.html', success_url = reverse_lazy('custom_auth:password_reset_done')), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html', success_url=reverse_lazy("custom_auth:password_reset_complete")),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),name='password_reset_complete'),
    path('user_change', views.RolesPermission.as_view(), name="add_roles_permissions"),
    path("user-datatable", views.UserListView.as_view(), name="user_datatable"),
    path("user-edit/<int:pk>", views.edit_user_details, name="edit_user_details"),
    path("edit-user-details", views.edit_user, name="edit_user"),
]
