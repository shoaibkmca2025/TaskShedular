from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY = [("L", "Low"), ("M", "Medium"), ("H", "High")]
    STATUS = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    CATEGORY = [
        ("work", "Work"),
        ("personal", "Personal"),
        ("health", "Health"),
        ("finance", "Finance"),
        ("education", "Education"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY, default="M")
    status = models.CharField(max_length=20, choices=STATUS, default="todo")
    category = models.CharField(max_length=20, choices=CATEGORY, default="other")
    due_date = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["done", "-priority", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.due_date and not self.done:
            return timezone.now() > self.due_date
        return False
