from django import forms
from . import models
from custom_auth import models as auth_models
from core import constants


class TodoForm(forms.ModelForm):
    class Meta:
        model = models.Todo
        fields = ["task_name", "priority_level", "assigned_to"]

        widgets = {
            "task_name": forms.TextInput(attrs={"class": "form-control"}),
            "priority_level": forms.RadioSelect(attrs={"class": "form-check"}),
            "assigned_to": forms.Select(attrs={"class": "form-control", "placeholder": "Choose a Trainee"})
        }