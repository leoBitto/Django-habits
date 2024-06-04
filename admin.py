# admin.py in habits app
from django.contrib import admin
from .models import Category, Habit, HabitEvent
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'colored_background', 'icon')
    search_fields = ['name']

    def colored_background(self, obj):
        return format_html(
            '<div style="background-color: {};">{}</div>',
            obj.color,
            obj.color
        )
    
    colored_background.short_description = 'Color'

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'is_positive')
    list_filter = ('category', 'is_positive')
    search_fields = ['name', 'category__name']

@admin.register(HabitEvent)
class HabitEventAdmin(admin.ModelAdmin):
    list_display = ('habit', 'start_date', 'start_time', 'end_date', 'end_time')
    list_filter = ('habit__category', 'start_date')
    search_fields = ['habit__name', 'start_date']

    # Aggiungi un campo di ricerca per il nome dell'abitudine
    raw_id_fields = ('habit',)
