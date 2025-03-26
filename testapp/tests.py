from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()

class TaskAPITest(APITestCase):
    """Test API endpoints for task management."""

    def setUp(self):
        """Setup test users and tasks before each test."""
        # Create users
        self.user1 = User.objects.create_user(username="testuser1", password="password123", email="user1@example.com")
        self.user2 = User.objects.create_user(username="testuser2", password="password123", email="user2@example.com")
        
        # Authenticate user
        self.client.force_authenticate(user=self.user1)

        # Create a task
        self.task = Task.objects.create(
            name="Test Task",
            description="A sample task for testing.",
            task_type="development",
            status="pending"
        )

    def test_create_task(self):
        """Test creating a new task."""
        url = "/api/create/"
        data = {
            "name": "New Task",
            "description": "This is a new task.",
            "task_type": "testing",
            "status": "pending"
        }
        response = self.client.post(url, data, format="json")

        print("Create Task Response:", response.status_code, response.data)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Task")

    def test_assign_task(self):
        """Test assigning a task to users."""
        url = "/api/assign/"
        data = {
            "task_id": self.task.id,
            "user_ids": [self.user1.id, self.user2.id]
        }
        response = self.client.post(url, data, format="json")

        print("Assign Task Response:", response.status_code, response.data)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        assigned_users = list(self.task.assigned_users.values_list("id", flat=True))
        self.assertIn(self.user1.id, assigned_users)
        self.assertIn(self.user2.id, assigned_users)

    def test_get_user_tasks(self):
        """Test retrieving tasks assigned to a user."""
        self.task.assigned_users.add(self.user1)  # Assign task to user1
        url = f"/api/user-tasks/{self.user1.id}/"
        response = self.client.get(url)

        print("Get User Tasks Response:", response.status_code, response.data)  # Debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.task.name)
