from django.db import models
from core import constants
from session_project.settings import AUTH_USER_MODEL
from custom_auth.models import CustomUser

# Create your models here.
class Todo(models.Model):
    task_name = models.CharField(max_length=255)
    priority_level = models.CharField(max_length=255, choices=constants.PRIORITY_CHOICES, default=constants.PRIORITY_LEVEL_LOW)
    is_completed = models.BooleanField(default=False)
    assigned_to =models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)