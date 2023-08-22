from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from ajax_datatable import AjaxDatatableView    
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from django.http import JsonResponse
from django.forms import model_to_dict
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm, UserRole
from session_project.settings import AUTH_USER_MODEL
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from session_project.settings import LOGIN_REDIRECT_URL
from core import template_utils, constants
from .models import CustomUser
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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


def customSiginPage(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {'form': form})


def customSignupPage(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_auth:login")
    else:
        form = SignUpForm()
    return render(request, "auth/registration.html", {'form': form})


class RolesPermission(LoginRequiredMixin, PermissionRequiredMixin, FormView, TemplateView):
    form_class = UserRole
    permission_required = "custom_auth.view_customuser"
    template_name = "auth/userchange.html"


class UserListView(AjaxDatatableView):
    model = CustomUser
    show_column_filters = False

    column_defs = [
        {"name": "id", "visible": False, "searchable": False, 'className': 'text-center'},
        {"name": "email", "visible": True, "searchable": True, 'className': 'text-center'},
        {"name": "role", "visible": True, "searchable": True, 'className': 'text-center'},
        {'name': 'action', 'title': 'Action', 'visible': True, 'searchable': False, 'orderable': False, 'className': 'text-center'},
    ]

    def customize_row(self, row, obj):
        buttons = ""
        if self.request.user.groups.filter(name="mentor").exists():
            buttons = template_utils.edit_button(reverse("custom_auth:edit_user_details", args=[obj.id])) \
                    + template_utils.delete_button(reverse("todo:todo_delete", args=[obj.id]))
        row['action'] = f'<div class="form-inline justify-content-center">{buttons}</div>'
        return 


def edit_user_details(request, pk):
    try:
        data = model_to_dict(get_object_or_404(CustomUser, id=pk))
        return JsonResponse(data, safe=False)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)
    


def edit_user(request):
    if request.method == "POST":
        form = UserRole(request.POST)
        if form.is_valid():
            mentor = Group.objects.get(name="mentor")
            record = CustomUser.objects.get(id=request.POST.get("record"))
            record.role = request.POST.get("role")
            record.groups.add(mentor)
            record.save()
            return JsonResponse({"status": "success"}, status=200)
        else:
            field_errors = form.errors.as_json()
            return JsonResponse({
                "status": "error",
                "field_errors": field_errors
            },status=404)
    data = CustomUser.objects.all()
    context = {
        "form": UserRole(),
        "data": data
    }
    return render(request, "todo/todo-list.html", context)