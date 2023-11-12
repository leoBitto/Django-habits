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


# class GoalForm(forms.ModelForm):
#     class Meta:
#         model = Goal
#         fields = ['target', 'description', 'start_date', 'end_date']

#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#             'description': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
#             'target': forms.NumberInput(attrs={'placeholder': 'Inserisci il numero di volte che desideri ripetere'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')

#         if start_date and end_date and start_date > end_date:
#             raise ValidationError('La data di inizio deve essere antecedente alla data di fine.')



class HabitEventForm(forms.ModelForm):
    class Meta:
        model = HabitEvent
        fields = ['habit', 'date', 'time', 'location']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
  
