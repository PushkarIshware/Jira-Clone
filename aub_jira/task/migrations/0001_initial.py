# Generated by Django 5.1.2 on 2024-10-22 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('story_points', models.IntegerField(blank=True, null=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(blank=True, related_name='task_labels', to='task.label')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_tasks', to='project.project')),
            ],
        ),
    ]