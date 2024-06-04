# models.py in habits app
from django.utils import timezone
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')  # Colore predefinito: blu
    icon = models.CharField(max_length=50, blank=True, null=True, default="fa-solid fa-")  # Nome dell'icona (es. "fas fa-running")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"  


class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class HabitEvent(models.Model):

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)  # Orario di inizio (opzionale)
    end_date = models.DateField(null=True, blank=True)  # Data di fine (opzionale)
    end_time = models.TimeField(null=True, blank=True)  # Orario di fine (opzionale)
    location = models.CharField(max_length=255, blank=True, null=True)  # Luogo dell'evento
    notes = models.TextField(blank=True, null=True)  # Note aggiuntive

    def __str__(self):
        return f"{self.habit.name} il {self.start_date} alle {self.start_time}"
    
    class Meta:
        ordering = ['start_date', 'start_time']


