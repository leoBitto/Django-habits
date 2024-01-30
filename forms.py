# habits/forms.py

from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta


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



class ReportForm(forms.Form):
    habit = forms.ModelChoiceField(queryset=Habit.objects.all(), empty_label="Select an habit", widget=forms.Select(attrs={'id': 'id_habit'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        # Imposta i valori di default per le date
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)
        self.fields['start_date'].initial = first_day_of_month
        self.fields['end_date'].initial = today


