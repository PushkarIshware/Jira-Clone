from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer, ProjectUpdateSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from aub_jira.permissions import CustomJWTTokenAuthentication
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

def get_generic_response():
    
    response = {
        'status_code': 200,
        'error': '',
        'message': '',
        'data': '',
    }
    return response

class AddProject(CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [CustomJWTTokenAuthentication]

    def post(self, request):
        response = get_generic_response()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['message'] = "New project created successfully."
            response['status_code'] = status.HTTP_201_CREATED
            return JsonResponse(response)
        response['message'] = "error occured during creating new project"
        response['status_code'] = status.HTTP_302_FOUND
        response['error'] = serializer.errors
        return JsonResponse(response)

class ListProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [CustomJWTTokenAuthentication]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        
        user = self.request.user
        queryset = Project.objects.filter(owner=user)
        
        search_param = self.request.query_params.get('search', None)
        
        if search_param:
            queryset = queryset.filter(
                Q(title__icontains=search_param) |
                Q(description__icontains=search_param) |
                Q(owner__username__icontains=search_param)
            )
        return queryset

class ViewProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [CustomJWTTokenAuthentication]

    def get(self, request, pk):
        response = get_generic_response()

        try:
            project = Project.objects.get(id=pk, owner__email=request.user.email)
        except Exception as e:
            response['message'] = "No project found"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            return JsonResponse(response)
        else:
            serializer = self.get_serializer(project)
            response['message'] = "Project fetched"
            response['status_code'] = status.HTTP_200_OK
            response['data'] = serializer.data
            return JsonResponse(response)
            

class ModifyProject(UpdateAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def patch(self, request, pk):
        response = get_generic_response()

        try:
            project = Project.objects.get(id=pk, owner__email=request.user.email)
        except Exception as e:
            response['message'] = "You are no authorized user to modify given project"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            return JsonResponse(response)
        else:
            serializer = ProjectUpdateSerializer(project, data=request.data, partial=True) #request.user
            if serializer.is_valid():
                serializer.save()
                response['message'] = "Project updated"
                response['status_code'] = status.HTTP_200_OK
                return JsonResponse(response)
            response['message'] = "something went wrong"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            response['error'] = serializer.errors
            return JsonResponse(response)
            # if 'title' in self.request.data:
            #     project.title = self.request.data['title']
            
            # if 'description' in self.request.data:
            #     project.description = self.request.data['description']
            
            # if 'members' in self.request.data:
            #     members_emails = self.request.data['members']
                
            #     if isinstance(members_emails, str):
            #         members_emails = members_emails.strip('[]').split(',')

            #     members_emails = [email.strip() for email in members_emails]
                
            #     users = User.objects.filter(email__in=members_emails)

            #     project.members.add(*users)

            # project.save()

            # response['message'] = "Project entitie(s) has been modified"
            # response['status_code'] = status.HTTP_200_OK
            # return JsonResponse(response)
    

class DeleteProject(DestroyAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def delete(self, request, pk):
        response = get_generic_response()

        try:
            project = Project.objects.get(id=pk, owner__email=request.user.email)
        except Exception as e:
            response['message'] = "No project found"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            return JsonResponse(response)
        else:
            project.delete()
            response['message'] = "Project has been deleted"
            response['status_code'] = status.HTTP_200_OK
            return JsonResponse(response)