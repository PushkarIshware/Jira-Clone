from django.urls import path
from project.views import AddProject, ListProjects, ViewProject, ModifyProject, DeleteProject 

urlpatterns = [
    path('add-project', AddProject.as_view(), name='add_project'),
    path('projects/list', ListProjects.as_view(), name='list_projects'),
    path('project/<int:pk>', ViewProject.as_view(), name='view_project'),
    path('modify-project/<int:pk>', ModifyProject.as_view(), name='modify_project'),
    path('delete-project/<int:pk>', DeleteProject.as_view(), name='delete_project'),
]