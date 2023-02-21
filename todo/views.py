from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound

from todo.forms import ProjectForm, TaskForm, ProjectExecutorForm, SubTaskForm
from todo.models import Project, Task, User, SubTask


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
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    tasks = Task.objects.filter(project_id=project_id)
    progress = {}
    for task in tasks:
        progress[task.pk] = {
            'total': SubTask.objects.filter(task_id=task.pk).count(),
            'done': SubTask.objects.filter(task_id=task.pk, is_done=True).count(),
        }
        if progress[task.pk]['total'] == 0 or progress[task.pk]['done'] == 0:
            progress[task.pk]['percent'] = 20
        else:
            progress[task.pk]['percent'] = int(progress[task.pk]['done'] / progress[task.pk]['total'] * 100)
    print(progress)
    executors = list(project.executors.all())
    context = {
        'project': project,
        'tasks': tasks,
        'executors': executors,
        'progress': progress,
    }
    return render(request, 'todo/project_details.html', context)


@login_required()
def task_create(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    executors = project.executors.all()
    form_cont = tuple((user.pk, user.get_full_name()) for user in executors)
    form = TaskForm(request.POST or None, form_cont)
    if request.method == 'POST':
        task = Task()
        task.name = form.data['name']
        task.description = form.data['description']
        task.author = request.user
        task.executor = User.objects.get(pk=form.data['executor'])
        d_d = form.data['deadline_day']
        d_m = form.data['deadline_month']
        d_y = form.data['deadline_year']
        task.deadline = f'{d_y}-{d_m}-{d_d}'
        task.project_id = Project.objects.get(pk=project_id)
        task.save()
        return redirect('todo:project_details', project_id)
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'todo/task_create.html', context)


@login_required
def task_edit(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')

    task_old = get_object_or_404(Task, pk=task_id)
    executors = project.executors.all()
    form_cont = tuple((user.pk, user.get_full_name()) for user in executors)
    form = TaskForm(request.POST or None, form_cont,
                    initial={
                        'name':1245
                    })
    form.fields['name'].initial = '77777'
    print(form)

    if form.is_valid():
        task_old = get_object_or_404(Task, pk=task_id)
        task_new = form.save(commit=False)
        task_old.name = task_new.name
        task_old.description = task_new.description
        task_old.deadline = task_new.deadline
        task_old.is_done = task_new.is_done
        task_old.executor = task_new.executor
        task_old.save()
        return redirect('todo:project_details', project_id)
    task = get_object_or_404(Task, pk=task_id)
    context = {
        'task': task,
        'form': form,
        'is_edit': True,
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
def project_edit(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    project_old = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None,
                       files=request.FILES or None,
                       instance=project_old)
    if form.is_valid():
        project_old = get_object_or_404(Project, pk=project_id)
        project_new = form.save(commit=False)
        project_old.name = project_new.name
        project_old.description = project_new.description
        project_old.deadline = project_new.deadline
        project_old.save()
        return redirect('todo:project_details', project_id)
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'todo/project_create.html', context)


@login_required
def add_project_executor(request, project_id):
    form = ProjectExecutorForm(request.POST or None)
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
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


def task_details(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    task = get_object_or_404(Task, pk=task_id)
    subtasks = SubTask.objects.filter(task_id=task_id)
    context = {
        'task': task,
        'subtasks': subtasks,
    }
    return render(request, 'todo/task_details.html', context)


def subtask_create(request, **kwargs):
    project = Project.objects.get(pk=kwargs['project_id'])
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    form = SubTaskForm(request.POST or None)
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.author = request.user
        subtask.project_id = Project.objects.get(pk=kwargs['project_id'])
        subtask.task_id = Task.objects.get(pk=kwargs['task_id'])
        subtask.save()
        return redirect('todo:task_details', project_id=kwargs['project_id'], task_id=kwargs['task_id'])
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'todo/subtask_create.html', context)


def subtask_done(request, project_id, task_id, subtask_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    SubTask.objects.filter(pk=subtask_id).update(is_done=(F('is_done') + 1) % 2)
    return redirect('todo:task_details', project_id=project_id, task_id=task_id)


def subtask_delete(request, project_id, task_id, subtask_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    SubTask.objects.filter(pk=subtask_id).delete()
    return redirect('todo:task_details', project_id=project_id, task_id=task_id)


def task_delete(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    if request.user != project.author or request.user not in project.executors.all():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    Task.objects.filter(pk=task_id).delete()
    return redirect('todo:project_details', project_id=project_id)