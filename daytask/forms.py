from django import forms

from .models import Tasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = (
            "date", "name", "discription_task", "status_task", "result", "count_answer", "score", "tries")
