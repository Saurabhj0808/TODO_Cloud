
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from todo.models import Task
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Send task reminders to users for tasks due today'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        users = User.objects.all()
        for user in users:
            due_tasks = Task.objects.filter(user=user, due_date=today, completed=False)
            if due_tasks.exists():
                task_list = "\n".join([f"- {task.title}" for task in due_tasks])
                send_mail(
                    subject='Task Reminder: Tasks Due Today',
                    message=f'You have the following tasks due today:\n\n{task_list}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
