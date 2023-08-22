from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from .forms import TodoForm
from django.forms import model_to_dict
from .models import Todo
from ajax_datatable import AjaxDatatableView
from django.core.mail import send_mail
from core import template_utils
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def todo_list(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            if request.POST.get("record"):
                record = Todo.objects.get(id=request.POST.get("record"))
                record.task_name = request.POST.get("task_name")
                record.priority_level = request.POST.get("priority_level")
                record.assigned_to_id = request.POST.get("assigned_to")
                record.save()
                return JsonResponse({"status": "success"}, status=200)
            form.save()
            send_mail(
                "New Task",
                "A new task has been created",
                "from@example.com",
                [request.user.email],
                fail_silently=False,
            )
            return JsonResponse({"status": "success"}, status=200)
        else:
            field_errors = form.errors.as_json()
            return JsonResponse(
                {"status": "error", "field_errors": field_errors}, status=404
            )
    data = Todo.objects.all()
    context = {"form": TodoForm(), "data": data}
    return render(request, "todo/todo-list.html", context)


class TodoListView(AjaxDatatableView):
    model = Todo
    show_column_filters = False

    column_defs = [
        {
            "name": "id",
            "visible": False,
            "searchable": False,
            "className": "text-center",
        },
        {
            "name": "task_name",
            "visible": True,
            "searchable": True,
            "className": "text-center",
        },
        {
            "name": "assigned_to",
            "foreign_field": "assigned_to__email",
            "visible": True,
            "searchable": True,
            "className": "text-center",
        },
        {
            "name": "priority_level",
            "visible": True,
            "searchable": True,
            "className": "text-center",
        },
        {
            "name": "is_completed",
            "title": "Completion Status",
            "visible": True,
            "searchable": True,
            "className": "text-center",
        },
        {
            "name": "action",
            "title": "Action",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "className": "text-center",
        },
    ]

    def get_initial_queryset(self, request=None):
        if request.user.is_authenticated:
            return Todo.objects.filter(assigned_to__email=request.POST.get('assigned_user'))
        else:
            return Todo.objects.all()

    def customize_row(self, row, obj):
        buttons = template_utils.show_button(
            reverse("todo:todo_complete", args=[obj.id])
        )
        if self.request.user.has_perm("todo.change_todo"):
            buttons += template_utils.edit_button(
                reverse("todo:todo_update", args=[obj.id])
            )
        if self.request.user.has_perm("todo.delete_todo"):
            buttons += template_utils.delete_button(
                reverse("todo:todo_delete", args=[obj.id])
            )
        row[
            "action"
        ] = f'<div class="form-inline justify-content-center">{buttons}</div>'
        return


@login_required
def todo_complete(request, pk):
    try:
        data = get_object_or_404(Todo, id=pk)
        data.is_completed = not data.is_completed
        data.save()
        return JsonResponse({"status": "success"}, status=200)
    except Todo.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)


@login_required
@permission_required("todo.change_todo")
def todo_update(request, pk):
    try:
        data = model_to_dict(get_object_or_404(Todo, id=pk))
        return JsonResponse(data, safe=False)
    except Todo.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)


@login_required
@permission_required("todo.change_todo")
def todo_delete(request, pk):
    try:
        data = get_object_or_404(Todo, id=pk)
        data.delete()
        return JsonResponse({"status": "success"}, status=200)
    except Todo.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)
