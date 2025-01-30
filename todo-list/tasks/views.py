from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        return Task.objects.none()  

class TaskDetailView(DeleteView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tasks'

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')


    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("task-list")  
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

# Create your views here.
