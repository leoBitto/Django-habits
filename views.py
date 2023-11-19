# habits/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Habit, HabitEvent
from .forms import *

from django.db.models import Count, Avg
from plotly.offline import plot
import plotly.graph_objs as go
from .models import Habit, HabitEvent

def overview(request):
    # Calcola le statistiche
    total_habits = Habit.objects.count()
    total_events = HabitEvent.objects.count()
    
    # Media di eventi per abitudine
    avg_events_per_habit = HabitEvent.objects.values('habit__name').annotate(avg_events=Avg('id'))


    # Crea un istogramma per la media di eventi per abitudine
    habit_names = [item['habit__name'] for item in avg_events_per_habit]
    avg_events = [item['avg_events'] for item in avg_events_per_habit]
    habit_bar = go.Bar(x=habit_names, y=avg_events, name='Media Eventi per Abitudine')

    # Crea un grafico a torta per le categorie
    categories = Category.objects.all()
    category_pie = go.Pie(labels=[category.name for category in categories], values=[category.habit_set.count() for category in categories], name='Categorie')

    # Rendi i grafici Plotly in HTML
    habit_bar_chart = plot([habit_bar], output_type='div')
    category_pie_chart = plot([category_pie], output_type='div')

    # Creazione del contesto per il template
    context = {
        'total_habits': total_habits,
        'total_events': total_events,
        'avg_events_per_habit_chart': habit_bar_chart,
        'category_pie_chart': category_pie_chart,
    }

    # Renderizza il template 'habits/overview.html' con il contesto creato
    return render(request, 'habits/overview.html', context)


# category views

def category(request):
    categories = Category.objects.all()

    category_form = CategoryForm()
    category_form_dict = {}

    for category in categories:
        edit_category_form = CategoryForm(instance=category)
        category_form_dict[category] = edit_category_form

    context = {
        'categories': categories,
        'category_form': category_form,
        'category_form_dict': category_form_dict,
    }

    return render(request, 'habits/category.html', context)

 
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            color = form.cleaned_data['color']
            icon = form.cleaned_data['icon']

        Category.objects.create(
            name=name,
            color=color,
            icon=icon
        )
    return redirect('habits:category')

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)  # Ottieni la categoria
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  # Passa l'istanza della categoria al form
        if form.is_valid():
            form.save()  # Salva le modifiche
            return redirect('habits:category')
    else:
        form = CategoryForm(instance=category)
    return redirect('habits:category')

def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()

    return redirect('habits:category')

# habit views

# Adapted views for Habit model

def habit(request):
    habits = Habit.objects.all()

    habit_form = HabitForm()
    habit_form_dict = {}

    grouped_habits = {}
    for habit in habits:
        category = habit.category
        if category not in grouped_habits:
            grouped_habits[category] = []

        edit_habit_form = HabitForm(instance=habit)
        habit_form_dict = {'habit': habit, 'form': edit_habit_form}
        grouped_habits[category].append(habit_form_dict)


    context = {
        'habits': habits,
        'habit_form': habit_form,
        'habit_form_dict': habit_form_dict,
        'grouped_habits': grouped_habits,
    }

    return render(request, 'habits/habit.html', context)


def create_habit(request):
    if request.method == 'POST':
        habit_form = HabitForm(request.POST)
        habits = Habit.objects.all()
        habit_form_dict = {}

        for habit in habits:
            edit_habit_form = HabitForm(instance=habit)
            habit_form_dict[habit] = edit_habit_form

        context = {
            'habits': habits,
            'habit_form': habit_form,
            'habit_form_dict': habit_form_dict,
        }

        if habit_form.is_valid():
            habit = habit_form.save()  # Salva l'abitudine


            return redirect('habits:habit')  # Redirect alla lista delle abitudini o ad altra pagina desiderata
    
    # Se il form non è valido, aggiungi il form come contesto e lascia che il template gestisca gli errori
    return render(request, 'habits/habit.html', context)


def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)  
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)  
        if form.is_valid():
            form.save()  
            return redirect('habits:habit')
    else:
        form = HabitForm(instance=habit)
    return redirect('habits:habit')


def delete_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id)
        habit.delete()

    return redirect('habits:habit')


# habit event views

def habit_event(request):
    habit_events = HabitEvent.objects.all()

    habit_event_form = HabitEventForm()
    habit_event_form_dict = {}

    grouped_habit_events = {}
    for habit_event in habit_events:
        category = habit_event.habit.category
        if category not in grouped_habit_events:
            grouped_habit_events[category] = []

        edit_habit_event_form = HabitEventForm(instance=habit_event)
        habit_event_form_dict = {'habit': habit_event, 'form': edit_habit_event_form}
        grouped_habit_events[category].append(habit_event_form_dict)


    context = {
        'habit_events': habit_events,
        'habit_event_form': habit_event_form,
        'habit_event_form_dict': habit_event_form_dict,
        'grouped_habit_events': grouped_habit_events,
    }

    return render(request, 'habits/habit_event.html', context)


def create_habit_event(request):
    if request.method == 'POST':
        form = HabitEventForm(request.POST)
        
        if form.is_valid():
            habit = form.cleaned_data['habit']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            location = form.cleaned_data['location']

            HabitEvent.objects.create(
                habit=habit,
                date=date,
                time=time,
                location=location,
            )
            
    return redirect('habits:habit_event')


def edit_habit_event(request, habit_event_id):
    habit_event = get_object_or_404(HabitEvent, pk=habit_event_id)  
    if request.method == 'POST':
        form = HabitEventForm(request.POST, instance=habit_event)  
        if form.is_valid():
            form.save()  
            return redirect('habits:habit_event')
    else:
        form = HabitEventForm(instance=habit_event)
    return redirect('habits:habit_event')


def delete_habit_event(request, habit_event_id):
    if request.method == 'POST':
        habit_event = get_object_or_404(HabitEvent, id=habit_event_id)
        habit_event.delete()

    return redirect('habits:habit_event')