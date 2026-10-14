from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "category", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "What needs to be done?",
                "autocomplete": "off",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-textarea",
                "placeholder": "Add details about this task...",
                "rows": 3,
            }),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateTimeInput(attrs={
                "class": "form-input",
                "type": "datetime-local",
            }, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"].input_formats = ["%Y-%m-%dT%H:%M"]
