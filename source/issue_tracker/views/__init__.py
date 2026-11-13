from .projects import (
    ProjectCreationView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)
from .tasks import (
    TaskCreationView,
    TaskDeleteView,
    TaskDetailView,
    TaskUpdateView,
)

__all__ = [
    'ProjectListView',
    'ProjectDetailView',
    'ProjectCreationView',
    'ProjectUpdateView',
    'ProjectDeleteView',
    'TaskDetailView',
    'TaskCreationView',
    'TaskUpdateView',
    'TaskDeleteView',
]
