# habits/forms.py

from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import datetime


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
        fields = ['name', 'category', ]
    

class HabitEventForm(forms.ModelForm):
    class Meta:
        model = HabitEvent
        fields = ['habit', 'date', 'time', ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Imposta i valori di default per 'date' e 'time' come il momento attuale
        self.fields['date'].initial = datetime.now().strftime('%Y-%m-%d')
        self.fields['time'].initial = datetime.now().strftime('%H:%M')

  
