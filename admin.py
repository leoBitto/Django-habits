from django.contrib import admin
from .models import Category, Habit, HabitEvent#, Goal

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(HabitEvent)
class HabitEventAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'time', 'location')
