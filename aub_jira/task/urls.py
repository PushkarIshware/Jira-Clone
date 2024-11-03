from django.urls import path
from task.views import AddTask, ListTasks, ViewTask, ModifyTask, DeleteTask

urlpatterns = [
    path('add-task', AddTask.as_view(), name='add_task'),
    path('tasks/list', ListTasks.as_view(), name='list_tasks'),
    path('task/<int:pk>', ViewTask.as_view(), name='view_task'),
    path('modify-task/<int:pk>', ModifyTask.as_view(), name='modify_task'),
    path('delete-task/<int:pk>', DeleteTask.as_view(), name='delete_task'),
]