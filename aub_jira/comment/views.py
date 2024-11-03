from django.shortcuts import get_object_or_404
from rest_framework import generics
from task.models import Task
from .models import Comment
from django.db.models import Q
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from aub_jira.permissions import CustomJWTTokenAuthentication
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CommentSerializer, UpdateSerializer, TaskCommentSerializer
from rest_framework import status

User = get_user_model()

def get_generic_response():
    
    response = {
        'status_code': 200,
        'error': '',
        'message': '',
        'data': '',
    }
    return response

class AddComment(CreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [CustomJWTTokenAuthentication]

    def post(self, request):
        response = get_generic_response()
        user = self.request.user

        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():

            task_id = int(serializer.validated_data['task'].id)
            # task_id
            right_to_comment = Task.objects.filter(Q(project__owner=user) | Q(project__members=user)).values_list('id', flat=True).distinct()

            if task_id in right_to_comment:

                serializer.save()
                response['message'] = "New comment added"
                response['status_code'] = status.HTTP_201_CREATED
                return JsonResponse(response)
            
            response['message'] = "Permission Denied"
            response['error'] = "given user is not asscociated with this project. you cannot add comment"
            response['status_code'] = status.HTTP_403_FORBIDDEN
            return JsonResponse(response)
        response['message'] = "required fields are missing"
        response['status_code'] = status.HTTP_400_BAD_REQUEST
        response['error'] = serializer.errors
        return JsonResponse(response)


class ModifyComment(UpdateAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def patch(self, request, pk):
        response = get_generic_response()

        comment_id = pk
        serializer = UpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                rightful_comment_owner = Comment.objects.get(id=comment_id, user__email=request.user.email)
            except Exception as e:
                response['message'] = "comment not found"
                response['status_code'] = status.HTTP_404_NOT_FOUND
                return JsonResponse(response)
            else:
                if 'text' in self.request.data:
                    rightful_comment_owner.text = serializer.validated_data['text']
                
                rightful_comment_owner.save()

                response['message'] = "comment has been modified"
                response['status_code'] = status.HTTP_200_OK
                return JsonResponse(response)
        response['message'] = "please provide comment text"
        response['error'] = serializer.errors
        response['status_code'] = status.HTTP_204_NO_CONTENT
        return JsonResponse(response)
    
class DeleteComment(DestroyAPIView):
    permission_classes = [CustomJWTTokenAuthentication]

    def delete(self, request, pk):
        response = get_generic_response()
        comment_id = pk

        try:
            rightful_comment_owner = Comment.objects.get(id=comment_id, user__email=request.user.email)
        except Exception as e:
            response['message'] = "No comment found"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            return JsonResponse(response)
        else:
            rightful_comment_owner.delete()
            response['message'] = "comment has been deleted"
            response['status_code'] = status.HTTP_200_OK
            return JsonResponse(response)
        
class ViewTaskComments(ListAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [CustomJWTTokenAuthentication]
    pagination_class = PageNumberPagination  

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        
        task = get_object_or_404(Task, id=task_id)

        project = task.project

        user = self.request.user
        if user == project.owner or project.members.filter(id=user.id).exists():
            return Comment.objects.filter(task_id=task_id)
        else:
            return None
        
    def list(self, request, *args, **kwargs):
        response = get_generic_response()
        queryset = self.get_queryset()

        if queryset is None:
            response['status_code'] = status.HTTP_401_UNAUTHORIZED
            response['error'] = "Given user not authorized to view comments"
            return JsonResponse(response)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)