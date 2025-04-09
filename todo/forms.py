
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-slate-700 text-white rounded px-3 py-2 w-full'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'bg-slate-700 text-white rounded px-3 py-2 w-full'}),
            'priority': forms.Select(attrs={'class': 'bg-slate-700 text-white rounded px-3 py-2 w-full'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'bg-slate-700 text-white rounded px-3 py-2 w-full'
    }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'bg-slate-700 text-white rounded px-3 py-2 w-full'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
