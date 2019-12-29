from django import forms
from .models import Task, Task_flow


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.created_by = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['title'].required = True
        self.fields['status'].required = True
        self.fields['company'].required = True
        self.fields['task_type'].required = True
        self.fields['priority'].required = True
        self.fields['due_date'].required = False
        # self.fields['created_by'].initial = self.created_by

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


class TaskUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.created_by = kwargs.pop('user')
        super(TaskUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['title'].required = True
        self.fields['status'].required = True
        self.fields['priority'].required = True

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Task with this Title already exists.')
        return title

    class Meta:
        model = Task
        fields = {
            'title', 'status', 'priority', 'due_date', 'is_active', 'complete_date'
        }


class Task_flowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Task_flowForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if Task_flow.objects.filter(description=description).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Task with this Title already exists.')
        return description

    class Meta:
        model = Task_flow
        fields = {
            'description',
        }
