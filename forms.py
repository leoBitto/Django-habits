# habits/forms.py

from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'category', 'icon']


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['habit', 'target', 'description', 'start_date', 'end_date']


class HabitEventForm(forms.ModelForm):
    class Meta:
        model = HabitEvent
        fields = ['habit', 'date', 'time', 'completed', 'location']  
