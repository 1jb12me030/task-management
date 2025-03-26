from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, AssignTaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import logging

#  Get the custom user model dynamically
User = get_user_model()

# Configure logging
logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    API endpoints for Task management.
    """

    @action(detail=False, methods=['post'])
    def create_task(self, request):
        """
        Creates a new task.
        """
        try:
            serializer = TaskCreateSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save()
                logger.info(f"Task created: {task.name}")  # Log task creation
                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
            logger.warning(f"Task creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in create_task: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def assign_task(self, request):
        """
        Assigns a task to users.
        """
        try:
            serializer = AssignTaskSerializer(data=request.data)
            if serializer.is_valid():
                task = get_object_or_404(Task, id=serializer.validated_data['task_id'])
                users = User.objects.filter(id__in=serializer.validated_data['user_ids'])
                task.assigned_users.set(users)
                logger.info(f"Task {task.id} assigned to users {serializer.validated_data['user_ids']}")
                return Response({"message": "Task assigned successfully."}, status=status.HTTP_200_OK)
            logger.warning(f"Task assignment failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in assign_task: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def user_tasks(self, request, pk=None):
        """
        Retrieves tasks assigned to a specific user.
        """
        try:
            user = get_object_or_404(User, id=pk)
            tasks = user.tasks.all()
            logger.info(f"Retrieved tasks for user {pk}")
            return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error in user_tasks: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)