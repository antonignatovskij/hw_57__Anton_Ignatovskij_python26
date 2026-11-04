from django.contrib import admin

from issue_tracker.models import (
    Task,
    Type,
    Status,
)

admin.site.register(Task)
admin.site.register(Type)
admin.site.register(Status)
