from django import forms
from .models import Task

class AddTaskForm(forms.ModelForm):
    """ Form for new task creation  """
    class Meta:
        model = Task
        fields = ['name', 'description']


class EditTaskForm(forms.ModelForm):
    """ Form for new task creation  """
    class Meta:
        model = Task
        fields = ['name', 'description', 'done']
