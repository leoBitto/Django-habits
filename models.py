# models.py in habits app
from django.utils import timezone
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')  # Colore predefinito: blu
    icon = models.CharField(max_length=50, blank=True, null=True, default="fa-solid fa-")  # Nome dell'icona (es. "fas fa-running")

    def __str__(self):
        return self.name


class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class HabitEvent(models.Model):

    CHOICHES=[
        ('minutes','minutes'),
        ('repetition','repetition'),
        ('quantity','quantity'),
    ]

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)  # Campo per l'ora, può essere opzionale
    location = models.CharField(max_length=100, null=True, blank=True)  # Campo per la posizione, può essere opzionale
    value = models.PositiveIntegerField(null=True, blank=True, default=1)
    value_type = models.CharField(max_length=10,choices=CHOICHES)

    def __str__(self):
        return f"{self.habit.name} il {self.date}"


