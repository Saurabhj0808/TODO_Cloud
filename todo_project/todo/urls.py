from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]