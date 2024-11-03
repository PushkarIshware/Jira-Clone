from rest_framework import generics
from .models import Task, Project
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from aub_jira.permissions import CustomJWTTokenAuthentication
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import TaskSerializer

User = get_user_model()

def get_generic_response():
    
    response = {
        'status_code': 200,
        'error': '',
        'message': '',
        'data': '',
    }
    return response

class AddTask(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [CustomJWTTokenAuthentication]

    def post(self, request):
        response = get_generic_response()
        
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project_id = int(serializer.validated_data['project'].id)

            right_to_create = Project.objects.filter(Q(owner__email=request.user.email) | Q(members__email=request.user.email)).values_list('id', flat=True)

            if project_id in right_to_create:

                serializer.save()
                response['message'] = "New task created successfully."
                response['status_code'] = status.HTTP_201_CREATED
                return JsonResponse(response)
            
            response['message'] = "Permission Denied"
            response['error'] = "given user is not asscociated with this project. you cannot create task."
            response['status_code'] = status.HTTP_403_FORBIDDEN
            return JsonResponse(response)
        response['message'] = "error occured during creating new tasks"
        response['status_code'] = status.HTTP_302_FOUND
        response['error'] = serializer.errors
        return JsonResponse(response)
    

class ListTasks(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [CustomJWTTokenAuthentication]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(Q(project__owner=user) | Q(project__members=user)).distinct()
        
        # Apply filters
        project_ids = self.request.query_params.getlist('projects')
        if project_ids:
            queryset = queryset.filter(project__id__in=project_ids)

        label_values = self.request.query_params.getlist('labels')
        if label_values:
            queryset = queryset.filter(labels__overlap=label_values)
        
        filter_param = self.request.query_params.get('search', None)
        if filter_param:
            queryset = queryset.filter(
                Q(title__icontains=filter_param) |
                Q(description__icontains=filter_param) |
                Q(labels__icontains=filter_param)
            )
        
        return queryset
    
class ViewTask(RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [CustomJWTTokenAuthentication]

    def get(self, request, pk):
        response = get_generic_response()

        task_id = pk

        right_to_view = Task.objects.filter(Q(assignee__email=request.user.email) | Q(project__owner__email=request.user.email)).values_list('id', flat=True)
        
        if task_id in right_to_view:
            
            task = Task.objects.get(id=task_id)
            
            serializer = self.get_serializer(task)
            response['data'] = serializer.data
            response['message'] = "Task details fetched"
            response['status_code'] = status.HTTP_200_OK
            return JsonResponse(response)
        
        response['message'] = "Permission Denied"
        response['error'] = "given user is not asscociated with this project. you cannot view task."
        response['status_code'] = status.HTTP_403_FORBIDDEN
        return JsonResponse(response)
    

class ModifyTask(UpdateAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def patch(self, request, pk):
        response = get_generic_response()

        task_id = pk
        right_to_update = Task.objects.filter(Q(assignee__email=request.user.email) | Q(project__owner__email=request.user.email)).values_list('id', flat=True)
        print(right_to_update,'-----')
        if task_id in right_to_update:
            
            task = Task.objects.get(id=task_id)
            
            if 'title' in self.request.data:
                task.title = self.request.data['title']
            
            if 'description' in self.request.data:
                task.description = self.request.data['description']
            
            if 'story_points' in self.request.data:
                task.story_points = self.request.data['story_points']
            
            if "new_assignee" in self.request.data:
                # project_id = task.project.id
                # project_owner = task.project.owner.id
                project_members = task.project.members.values_list('id', flat=True)
                
                if int(self.request.data['new_assignee']) in project_members:
                    try:
                        users = User.objects.get(id=int(self.request.data['new_assignee']))
                    except Exception as e:
                        response['message'] = "User not found"
                        response['status_code'] = status.HTTP_403_FORBIDDEN
                        return JsonResponse(response)
                    else:
                        task.assignee = users
                else:
                    response['message'] = "New assignee is not associated with this project"
                    response['status_code'] = status.HTTP_403_FORBIDDEN
                    return JsonResponse(response)

            if "labels" in self.request.data:
                if isinstance(self.request.data['labels'], str):
                    labels = self.request.data['labels'].strip('[]').split(',')
                
                for each in labels:
                    task.labels.append(each.strip())

            task.save()

            response['message'] = "Task entitie(s) has been modified"
            response['status_code'] = status.HTTP_200_OK
            return JsonResponse(response)
        

class DeleteTask(DestroyAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def delete(self, request, pk):
        response = get_generic_response()
        task_id = pk
        right_to_delete = Task.objects.filter(project__owner__email=request.user.email).values_list('id', flat=True)

        if task_id in right_to_delete:

            try:
                task = Task.objects.get(id=pk)
            except Exception as e:
                response['message'] = "No task found"
                response['status_code'] = status.HTTP_404_NOT_FOUND
                return JsonResponse(response)
            else:
                task.delete()
                response['message'] = "task has been deleted"
                response['status_code'] = status.HTTP_200_OK
                return JsonResponse(response)
        
        response['message'] = "Permission Denied"
        response['error'] = "given user is not asscociated with this project. you cannot delete task."
        response['status_code'] = status.HTTP_403_FORBIDDEN
        return JsonResponse(response)

        