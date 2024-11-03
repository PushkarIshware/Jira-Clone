from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    # task = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'text', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class UpdateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'created_at']