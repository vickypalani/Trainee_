from django.urls import path
from . import views


urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("todo-datatable", views.TodoListView.as_view(), name="todo_datatable"),
    path("todo-complete/<int:pk>", views.todo_complete, name="todo_complete"),
    path("todo-update/<int:pk>", views.todo_update, name="todo_update"),
    path("todo-delete/<int:pk>", views.todo_delete, name="todo_delete"),
]
