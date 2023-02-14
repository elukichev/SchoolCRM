from django.forms import ModelForm

from django import forms
from .models import Project


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
