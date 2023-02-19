from django.forms import ModelForm, Form

from django import forms
from django.shortcuts import get_object_or_404

from .models import Project, Task, SubTask


class ProjectForm(ModelForm):
    deadline = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Project
        fields = ('name', 'description', 'deadline')
        labels = {'description': 'Описание проекта',
                  'deadline': 'Время сдачи проекта',
                  'name': 'Название проекта'}
        help_text = {'description': 'Введите описание проекта',
                     'deadline': 'Выберите дату',
                     'name': 'Введите название проекта'}


class TaskForm(Form):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['executor'] = forms.ChoiceField(choices=args[1])

    name = forms.CharField(
        label='Введите название задачи',
        max_length=150,
        required=True,
    )
    description = forms.CharField(
        label='Введите описание задачи',
        required=True,
        widget=forms.Textarea,
    )
    deadline = forms.DateField(widget=forms.SelectDateWidget())


    """executor = forms.ModelChoiceField(queryset=None)

    def __init__(self, *project_id):
        super(TaskForm, self).__init__()
        self.project_id = project_id[1]
        self.project = get_object_or_404(Project, pk=self.project_id)
        self.fields['executor'].queryset = self.project.executors.all()

    deadline = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Task
        fields = ('name', 'description', 'executor', 'deadline')
        labels = {'description': 'Описание проекта',
                  'deadline': 'Время сдачи проекта',
                  'name': 'Название проекта'}
        help_text = {'description': 'Введите описание проекта',
                     'deadline': 'Выберите дату',
                     'name': 'Введите название проекта'}"""


class SubTaskForm(ModelForm):
    executor = forms.ModelMultipleChoiceField(queryset=None)
    def __init__(self, *project_id):
        super(SubTaskForm, self).__init__()
        self.project_id = project_id[1]
        self.project = get_object_or_404(Project, pk=self.project_id)
        self.fields['executor'] = list(self.project.executors.all())


    deadline = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = SubTask
        fields = ('name', 'description', 'deadline', 'executor')
        labels = {'description': 'Описание проекта',
                  'deadline': 'Время сдачи проекта',
                  'name': 'Название проекта'}
        help_text = {'description': 'Введите описание проекта',
                     'deadline': 'Выберите дату',
                     'name': 'Введите название проекта'}


class ProjectExecutorForm(Form):
    username = forms.CharField(
        label='Введите имя пользователя',
        max_length=150
    )
