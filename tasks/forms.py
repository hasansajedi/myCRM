from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['title'].required = True
        self.fields['status'].required = True
        self.fields['company'].required = True
        self.fields['task_type'].required = True
        self.fields['priority'].required = True
        self.fields['due_date'].required = False

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Task with this Title already exists.')
        return title

    class Meta:
        model = Task
        fields = {
            'title', 'status', 'priority', 'due_date', 'company', 'task_type', 'is_active'
        }
