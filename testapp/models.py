from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

#  Custom User Model with name & mobile
class CustomUser(AbstractUser):
    
    """
    Custom user model that extends Django's default AbstractUser.
    Additional fields:
    - name: Full name of the user.
    - mobile: Mobile number (optional, unique).
    """
    
    name = models.CharField(max_length=255)  # Full Name
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True)  # Mobile Number

    def __str__(self):
        return self.username

#  Task Model with Many-to-Many Relationship
class Task(models.Model):
    
    """
    Task model representing a task assigned to one or more users.

    Fields:
    - name: Task title/name.
    - description: Detailed description of the task.
    - created_at: Timestamp of when the task was created.
    - task_type: Optional field indicating the type/category of task.
    - completed_at: Timestamp of when the task was completed (if applicable).
    - status: Current status of the task (Pending, In Progress, or Completed).
    - assigned_users: Many-to-Many relation linking the task to multiple users.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    def __str__(self):
        return self.name
