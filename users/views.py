from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


# Create your views here.
class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('todo:index')
    template_name = 'users/signup.html'