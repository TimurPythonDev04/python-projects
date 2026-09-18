from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%d'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
