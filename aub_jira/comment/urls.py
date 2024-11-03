from django.urls import path
from comment.views import AddComment ,ModifyComment, DeleteComment, ViewTaskComments

urlpatterns = [
    path('add-comment', AddComment.as_view(), name='add_comment'),
    # path('tasks/list', ListTasks.as_view(), name='list_comment'),
    path('task-comments/<int:task_pk>', ViewTaskComments.as_view(), name='view_task_comment'),
    path('modify-comment/<int:pk>', ModifyComment.as_view(), name='modify_comment'),
    path('delete-comment/<int:pk>', DeleteComment.as_view(), name='delete_comment'),
]