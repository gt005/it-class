from django import forms

from .models import EducationTask


class CreateNewTaskDatesForm(forms.ModelForm):
    class Meta:
        model = EducationTask
        fields = (
            'start_time',
            'end_time',
            'task_level',
            'task_name',
            'description_task',
            'input_format',
            'output_format',
            'photo_1',
            'photo_2',
            'photo_3',
            'example_input_1',
            'example_output_1',
            'example_input_2',
            'example_output_2',
            'example_input_3',
            'example_output_3',
        )