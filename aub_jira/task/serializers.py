from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from django.http import JsonResponse
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

class ViewTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'story_points', 'assignee', 'project', 'labels']

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.ReadOnlyField(source='assignee.email')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'story_points', 'assignee', 'project', 'labels']

    def create(self, validated_data):
        validated_data['assignee'] = self.context['request'].user
        return super().create(validated_data)
    

# class TaskUpdateSerializer(serializers.ModelSerializer):
#     labels = serializers.ListField(
#         write_only=True,
#         required=False
#     )
#     assignee = serializers.IntegerField(required=False)

#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'story_points', 'assignee', 'labels']

#     def update(self, instance, validated_data):

#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.story_points = validated_data.get('story_points', instance.story_points)

#         # if 'owner' in validated_data:
#         #     raise serializers.ValidationError("You cannot change owner of the project") 

#         if 'labels' in validated_data:
#             labels = validated_data.pop('labels', [])
#             print(labels,'-----',type(labels))
#             if len(labels) > 0:           
#                 actual_labels = labels[0]
#                 list_of_labels = actual_labels.split(",")

#                 for each in labels:
#                     instance.labels.append(each.strip())

#         if "assignee" in validated_data:
#             response = get_generic_response()
#             right_to_assign = self.context.get('right_to_assign')
#             print(right_to_assign,'-----',validated_data['assignee'], type(validated_data['assignee']))
            
#             if int(validated_data['assignee']) in right_to_assign:
#                 print("insdie")
#                 try:
#                     users = User.objects.get(id=int(validated_data['assignee']))
#                 except Exception as e:
#                     response['message'] = "User not found"
#                     response['status_code'] = status.HTTP_403_FORBIDDEN
#                     return JsonResponse(response)
#                 else:
#                     instance.assignee = users
#             else:
#                 response['message'] = "New assignee is not associated with this project"
#                 response['status_code'] = status.HTTP_403_FORBIDDEN
#                 return JsonResponse(response)
        
#         instance.save()
#         return instance