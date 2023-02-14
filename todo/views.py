from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from todo.forms import ProjectForm
from todo.models import Project


def index(request):
    template = 'todo/index.html'
    return render(request, template)

@login_required()
def project_list(request):
    template = 'todo/project_list.html'
    projects_list = Project.objects.filter(author=request.user.pk)
    print(projects_list)
    print(request.user.pk)
    context = {
        'projects_list': projects_list,
    }
    return render(request, template, context)


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


def project_details(request, slug):
    return HttpResponse(f'Информация о проекте {slug}')

