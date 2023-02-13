from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'todo/index.html'
    return render(request, template)


def project_list(request):
    return HttpResponse('Список проектов пользователя')


def project_details(request, slug):
    return HttpResponse(f'Информация о проекте {slug}')

