# task-management

A RESTful Task Management API built using Django & Django REST Framework. This API allows users to create, assign, and retrieve tasks with authentication via Token Authentication.

# Installation and setup
git clone https://github.com/your-username/task-management.git
cd task-management
# To create virtual environment
python -m venv venv  # Create virtual environment
venv\Scripts\activate  # Windows

# install dependencies 
pip install -r requirements.txt
# Create a .env file in the project root and add:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
# Apply Migrations
python manage.py migrate
# Create a Superuser
python manage.py createsuperuser
# Run the Server
python manage.py runserver
# API will be available at:
 http://127.0.0.1:8000/api/
 ## API Endpoints
# 1.Obtain Auth Token
URL: /api/api-token-auth/
Method: POST
# Request
{
  "username": "admin",
  "password": "adminpassword"
}
# Response 
{
  "token": "auth-token"
}
# 2. Create a Task
URL: /api/create/
Method: POST
Headers: Authorization: Token your-auth-token
# Request:
{
  "name": "New Task",
  "description": "Task details...",
  "task_type": "testing",
  "status": "pending"
}
# Response :
{
  "id": 1,
  "name": "New Task",
  "description": "Task details...",
  "status": "pending"
}
# 3. Assign a Task
URL: /api/assign/
Method: POST
Headers: Authorization: Token your-auth-token
# Request
{
  "task_id": 1,
  "user_ids": [2, 3]
}
# Response
{
  "message": "Task assigned successfully."
}
# 4. Get Tasks Assigned to a User
URL: /api/user-tasks/{user_id}/
Method: GET
Headers: Authorization: Token your-auth-token
# Response:
[
    {
        "id": 2,
        "assigned_users": [
            {
                "id": 2,
                "username": "admin1",
                "email": "",
                "mobile": null
            },
            {
                "id": 3,
                "username": "admin11",
                "email": "",
                "mobile": null
            }
        ],
        "name": "Complete Project",
        "description": "Finish the Django project by the deadline",
        "created_at": "2025-03-25T19:15:16.967792Z",
        "task_type": "urgent",
        "completed_at": null,
        "status": "pending"
    }
]

## Running Tests
python manage.py test
## Build & Run Docker Container
docker build -t django-task-api .
docker run -p 8000:8000 django-task-api

******************************************* All set ! Thank You ! *******************************
