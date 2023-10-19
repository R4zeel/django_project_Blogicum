from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import MyUserCreationForm

from django.urls import reverse_lazy

class Registration(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('blod:index')