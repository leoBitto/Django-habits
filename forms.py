# habits/forms.py

from django import forms
from .models import *
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color','icon']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'category', 'is_positive']
        widgets = {
            'is_positive': forms.CheckboxInput(),
        }


class HabitEventForm(forms.ModelForm):
    class Meta:
        model = HabitEvent
        fields = ['habit', 'date', 'time', 'location', 'value', 'value_type']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
  
