from django.db import models
from django.contrib.auth import get_user_model
from project.models import Project
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    story_points = models.IntegerField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assigned_to")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_tasks")
    labels = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    def __str__(self):
        # return self.title
        return f'title: {self.title}, assignee: {str(self.assignee.email)}'