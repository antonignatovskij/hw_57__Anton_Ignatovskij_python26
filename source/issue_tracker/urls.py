from django.urls import path
from issue_tracker.views import (
    TasksView,
    TaskDetailView,
    TaskCreationView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path('', TasksView.as_view()),

    path('tasks/',TasksView.as_view(), name='tasks_list'),

    path('tasks/<int:pk>/',TaskDetailView.as_view(), name='tasks_detail'),

    path('tasks/<int:pk>/update/',TaskUpdateView.as_view(), name='tasks_update'),

    path('tasks/create/',TaskCreationView.as_view(), name='tasks_create'),

    path('tasks/<int:pk>/delete/',TaskDeleteView.as_view(), name='tasks_delete'),
]