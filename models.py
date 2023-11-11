# models.py in habits app

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')  # Colore predefinito: blu

    def __str__(self):
        return self.name

class Habit(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True, null=True)  # Nome dell'icona (es. "fas fa-running")
    

    def __str__(self):
        return self.name

class Goal(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    target = models.IntegerField()  # Numero di volte che si vuole praticare l'abitudine al mese
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Goal per {self.habit.name} ({self.start_date} - {self.end_date})"

class HabitEvent(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)  # Campo per l'ora, può essere opzionale
    completed = models.BooleanField(default=False)  # Indica se l'abitudine è stata completata
    location = models.CharField(max_length=100, null=True, blank=True)  # Campo per la posizione, può essere opzionale

    def __str__(self):
        return f"{self.habit.name} il {self.date}"
