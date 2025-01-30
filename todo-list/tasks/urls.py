from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", TaskListView.as_view(), name="task-list"),
    path('', TaskListView.as_view(), name = 'task-list') ,
    path('task/<int:pk>/', TaskDetailView.as_view(), name = 'task-detail'),
    path('create/', TaskCreateView.as_view(), name = 'task-create') ,
    path('update/<int:pk>/', TaskUpdateView.as_view(), name = 'task-update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name = 'task-delete'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]