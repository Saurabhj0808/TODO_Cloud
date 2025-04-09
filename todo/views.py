from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task
from .forms import TaskForm, CustomUserCreationForm


def send_task_created_email(user_email, task):
    send_mail(
        subject="New Task Added",
        message=f"A new task titled '{task.title}' has been added with priority {task.priority} and due on {task.due_date}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


def send_welcome_email(user_email):
    send_mail(
        subject="Welcome to the To-Do App!",
        message="Thank you for signing up. Start adding tasks and stay organized!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Sending welcome email to", user.email)  # optional debug
            send_welcome_email(user.email)
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
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
            send_task_created_email(request.user.email, task)
            return redirect('task_list')
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})


@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id, user=request.user).delete()
    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            # 🔔 Send edit email here
            send_mail(
                subject="Task Updated",
                message=f"Your task '{task.title}' has been updated.\n\nNew Priority: {task.priority}\nNew Due Date: {task.due_date}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True
            )

            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            send_task_created_email(request.user.email, task)
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/edit_task.html', {'form': form})
