from django.urls import path
from .views import TaskViewSet
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create/', TaskViewSet.as_view({'post': 'create_task'}), name='create-task'),
    path('assign/', TaskViewSet.as_view({'post': 'assign_task'}), name='assign-task'),
    path('user-tasks/<int:pk>/', TaskViewSet.as_view({'get': 'user_tasks'}), name='user-tasks'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
