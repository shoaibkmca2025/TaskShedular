from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "priority", "status", "category", "done", "due_date", "created_at"]
    list_filter = ["priority", "status", "category", "done"]
    search_fields = ["title", "description"]
    list_editable = ["done", "status", "priority"]
