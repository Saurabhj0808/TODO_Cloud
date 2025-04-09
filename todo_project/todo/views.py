from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task
from .forms import TaskForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id, user=request.user).delete()
    return redirect('task_list')