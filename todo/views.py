from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from todo.forms import ProjectForm, TaskForm, ProjectExecutorForm
from todo.models import Project, Task, User


def index(request):
    template = 'todo/index.html'
    # return render(request, template
    return redirect('/projects')

@login_required()
def project_list(request):
    template = 'todo/project_list.html'
    projects_list = Project.objects.filter(author=request.user.pk)
    context = {
        'projects_list': projects_list,
    }
    return render(request, template, context)


@login_required()
def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    #executors = User.objects.filter()
    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'todo/project_details.html', context)


@login_required()
def task_create(request, **kwargs):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.author = request.user
        task.project_id = Project.objects.get(pk=kwargs['project_id'])
        task.save()
        return redirect('todo:index')
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'todo/task_create.html', context)


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.author = request.user
        project.save()
        return redirect('todo:index')
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'todo/project_create.html', context)


@login_required
def add_project_executor(request, project_id):
    form = ProjectExecutorForm(request.POST or None)
    project = Project.objects.get(pk=project_id)
    context = {
        'form': form,
        'project_name': project.name,
        'attantion': '',
    }
    if form.is_valid():
        username = form.cleaned_data['username']
        if username in list(User.objects.values_list("username", flat=True)):
            user = User.objects.get(username=username)
            project.executors.add(user)
            return redirect('todo:index')
        context['attantion'] = 'Такого пользователя нет'
    return render(request, 'todo/add_executor.html', context)