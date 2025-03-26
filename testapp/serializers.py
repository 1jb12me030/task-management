from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

# Get CustomUser model dynamically
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Fields:
    - id: Unique identifier for the user.
    - username: User's username.
    - email: User's email address.
    - mobile: Mobile number of the user (custom field from CustomUser model).
    """

    class Meta:
        model = User  # Use CustomUser instead of default User
        fields = ['id', 'username', 'email', 'mobile']  # Include 'mobile' field


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    - assigned_users: Nested representation of assigned users using UserSerializer (read-only).
    - All other Task model fields are included.

    This serializer is used for retrieving task details along with user assignments.
    """

    assigned_users = UserSerializer(many=True, read_only=True)  # Serialize assigned users

    class Meta:
        model = Task
        fields = '__all__'  # Include all Task model fields


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Task.

    Fields:
    - name: Task title.
    - description: Task details.
    - task_type: Optional category/type of task.
    - status: Status of the task.

    Note: assigned_users is not included since users are assigned separately.
    """

    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type', 'status']


class AssignTaskSerializer(serializers.Serializer):
    """
    Serializer for assigning users to a task.

    Fields:
    - task_id: ID of the task to which users will be assigned.
    - user_ids: List of user IDs to be assigned to the task.

    This is a custom serializer (not model-based) used for handling task-user assignments.
    """

    task_id = serializers.IntegerField(help_text="ID of the task to assign users to.")
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), help_text="List of user IDs to be assigned to the task."
    )
