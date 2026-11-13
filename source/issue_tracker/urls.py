from django.urls import path
from issue_tracker.views import (
    ProjectCreationView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    TaskDetailView,
    TaskCreationView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects_list'),
    path('projects/create/', ProjectCreationView.as_view(), name='projects_create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='projects_detail'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='projects_delete'),
    path(
        'projects/<int:project_pk>/tasks/create/',
        TaskCreationView.as_view(),
        name='tasks_create',
    ),
    path('tasks/<int:pk>/',TaskDetailView.as_view(), name='tasks_detail'),
    path('tasks/<int:pk>/update/',TaskUpdateView.as_view(), name='tasks_update'),
    path('tasks/<int:pk>/delete/',TaskDeleteView.as_view(), name='tasks_delete'),
]
