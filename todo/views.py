from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from todo.forms import ProjectForm


def index(request):
    template = 'todo/index.html'
    return render(request, template)


def project_list(request):
    return HttpResponse('Список проектов пользователя')


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('todo:index')
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'todo/project_create.html', context)


def project_details(request, slug):
    return HttpResponse(f'Информация о проекте {slug}')

