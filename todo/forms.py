from django import forms
from . import models


class TodoForm(forms.ModelForm):
    class Meta:
        model = models.Todo
        fields = ["task_name", "priority_level"]

        widgets = {
            "task_name": forms.TextInput(attrs={"class": "form-control"}),
            "priority_level": forms.RadioSelect(attrs={"class": "form-check"}),
        }