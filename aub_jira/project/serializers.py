from rest_framework import serializers
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    # members = serializers.ListField(
    #     # child=serializers.EmailField(), 
    #     write_only=True, required=False
    # )
    # title = serializers.CharField(required=False, blank=True)
    # description = serializers.CharField(required=False, blank=True)
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'owner', 'members']
        read_only_fields = ['owner']  # Owner cannot be updated

    # def get_members(self, obj):
    #     return obj.members.values_list('email', flat=True)
    
    def get_members(self, obj):
        return [member.email for member in obj.members.all()]

    def create(self, validated_data):
        # Set the project owner as the current authenticated user
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    # def create(self, validated_data):
    #     # Remove the members list from the validated data
    #     members_emails = validated_data.pop('members', [])
        
    #     # Set the owner as the current authenticated user
    #     validated_data['owner'] = self.context['request'].user
        
    #     # Create the project
    #     project = super().create(validated_data)
        
    #     if members_emails:
    #         users = User.objects.filter(email__in=members_emails)
    #         print(users.count())
    #         project.members.add(*users)
        
    #     return project

    # def update(self, instance, validated_data):
    #     # Update only the fields provided
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
        
    #     # Handle members update
    #     # members_emails = validated_data.get('members', None)
    #     # if members_emails:
    #     #     users = User.objects.filter(email__in=members_emails)
    #     #     instance.members.set(users)

    #     instance.save()
    #     return instance


class ProjectUpdateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = ('title', 'description', 'members',)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        
        # if 'owner' in validated_data:
        #     raise serializers.ValidationError("You cannot change owner of the project") 

        if 'members' in validated_data:
            members_emails = validated_data.pop('members', [])
            if len(members_emails) > 0:           
                actual_emails = members_emails[0]
                list_of_emails = actual_emails.split(",")
                list_of_emails = [each.strip() for each in list_of_emails]

                users = User.objects.filter(email__in=list_of_emails)
                instance.members.add(*users)
        
        instance.save()
        return instance