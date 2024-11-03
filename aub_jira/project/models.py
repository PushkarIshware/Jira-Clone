from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_owner")
    members = models.ManyToManyField(User, related_name="project_member", blank=True)
    
    def __str__(self):
        return f'title: {self.title}, owner: {str(self.owner.email)}'