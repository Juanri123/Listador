from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import task 

class CustomLoginView(LoginView):
    template_name = 'lister/ingresar.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tareas')
    
class RegisterPage(FormView):
    template_name = 'lister/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is None:
            login(self.request, usuario)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('Tareas')
        return super(RegisterPage, self).get(*args, **kwargs)



class lista(LoginRequiredMixin, ListView):
    model = task
    context_object_name = "Tareas"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['Tareas'] = context['Tareas'].filter(usuario=self.request.user)
        context['count'] = context['Tareas'].filter(hecho=False).count()

        search_input = self.request.GET.get('Buscador') or ''
        if search_input:
            context['Tareas'] = context['Tareas'].filter(titulo_startswith=search_input)

        context['search_input'] = search_input
        return context
    
    


class Detalles(LoginRequiredMixin, DetailView):
    model = task
    context_object_name = 'Task'
    template_name = 'lister/task.html'

   

class TaskCreate(LoginRequiredMixin, CreateView):
    model = task
    fields = ['titulo', 'descripcion', 'hecho']
    success_url = reverse_lazy('tareas')

    def form_invalid(self, form):
        form.instance.usuario = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ['titulo', 'descripcion', 'hecho']
    success_url = reverse_lazy('tareas')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = task
    context_object_name = 'Task'
    success_url = reverse_lazy('tareas')


