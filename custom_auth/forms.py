from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from .models import CustomUser


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label= "Password", widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}), required=True)
    password2 = forms.CharField(label= "Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}), required=True)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs = {
                'placeholder': 'Email',
                "class": 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'Password',
                "class": 'form-control'
            }
        )
    )
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

class UserRole(forms.ModelForm):
    email = forms.ModelChoiceField(label="Email", 
        queryset=CustomUser.objects.all())
    class Meta:
        model = CustomUser
        fields = ["role"]

        widgets = {
            "email": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }