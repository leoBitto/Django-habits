# habits/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Habit, HabitEvent
from .forms import *
from django.http import HttpResponse
import pandas as pd
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
from .utils import *


def index(request):
    """
    View for the index page.

    - Retrieves today's and yesterday's habit events.
    - Generates a pie chart 
    - Handles errors and displays corresponding messages.

    Args:
        request: Django HttpRequest object.

    Returns:
        Rendered template with the context.
    """
    try:
        # Retrieve today's and yesterday's habit events
        events_of_today = HabitEvent.objects.filter(start_date=date.today())
        events_of_yesterday = HabitEvent.objects.filter(start_date=date.today() + timedelta(days=-1))

        # Call the auxiliary function to create the pie chart
        success_pie_chart, pie_chart_html = generate_pie_chart(date.today(), date.today())

        # Calculate the heatmap of correlations
        #success_heatmap, heatmap_html = generate_heat_map(date(2024, 1, 1), date.today())

        # Check if any function call failed and show corresponding messages
        if not all([
            #success_heatmap, 
            success_pie_chart
         ]):
            error_messages = [message for success, message in [
                #(success_heatmap, "Error generating heatmap."),
                (success_pie_chart, "Error generating pie chart."),
            ] if not success]

            for error_message in error_messages:
                messages.warning(request, error_message)

        # Create the context for the template
        context = {
            'habit_event_form': HabitEventForm(),
            'events_of_today': events_of_today,
            'events_of_yesterday': events_of_yesterday,
            'pie_chart_html': pie_chart_html,
            #'heatmap_html': heatmap_html,
            'report_form': ReportForm(),
        }

    except Exception as e:
        messages.error(request, f"Error processing data for the index view: {str(e)}")
        context = {}

    # Render the 'habits/index.html' template with the created context
    return render(request, 'habits/index.html', context)

def create_report(request):
    """
    View for creating a habit report.

    - Retrieves form data for habit, start date, and end date.
    - Generates hourly and daily charts, pie chart, and heatmap.
    - Handles errors and displays corresponding messages.

    Args:
        request: Django HttpRequest object.

    Returns:
        Rendered template with the context.
    """
    try:
        if request.method == 'POST':
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                habit = report_form.cleaned_data['habit']
                start_date = report_form.cleaned_data['start_date']
                end_date = report_form.cleaned_data['end_date']

        # Call functions to generate charts and handle errors
        success_hourly_chart, hourly_html = generate_hourly_chart(start_date, end_date, habit.id)
        success_daily_chart, daily_html = generate_daily_chart(start_date, end_date, habit.id)


        # Check if any function call failed and show corresponding messages
        if not all([success_hourly_chart, success_daily_chart]):
            error_messages = [message for success, message in [
                (success_hourly_chart, "Error generating hourly chart."),
                (success_daily_chart, "Error generating daily chart."),

            ] if not success]

            for error_message in error_messages:
                messages.warning(request, error_message)

        # Ottenere gli HabitEvent associati all'abitudine nel periodo specificato
        habit_events = HabitEvent.objects.filter(
            habit=habit,
            date__range=(start_date, end_date)
        )

        total_events = habit_events.count()
        average_events_per_day = total_events / (end_date - start_date).days if total_events > 0 else 0


        # Create the context for the template
        context = {
            'hourly_html': hourly_html,
            'daily_html': daily_html,
            'total_events': total_events,
            'average_events_per_day': round(average_events_per_day, 2),
        }

    except Exception as e:
        messages.error(request, f"Error processing data for the create_report view: {str(e)}")
        context = {}

    # Render the 'habits/report.html' template with the created context
    return render(request, 'habits/report.html', context)

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
            messages.success(request, 'Category successfully created')
        else:
            messages.info(request, "Couldn't create Category")
    return redirect('habits:category')

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)  # Ottieni la categoria
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  # Passa l'istanza della categoria al form
        if form.is_valid():
            form.save()  # Salva le modifiche
            messages.success(request, 'Category successfully edited')
            return redirect('habits:category')
        else:
            messages.error(request, "Couldn't edit Category")
    else:
        form = CategoryForm(instance=category)
    return redirect('habits:category')

def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category successfully eliminated')
    else:
        messages.error(request, "Couldn't eliminate Category")
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
            messages.success(request, "Habit created")

            return redirect('habits:habit')  # Redirect alla lista delle abitudini o ad altra pagina desiderata
    
    # Se il form non è valido, aggiungi il form come contesto e lascia che il template gestisca gli errori
    return render(request, 'habits/habit.html', context)


def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)  
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)  
        if form.is_valid():
            form.save()  
            messages.success(request, "Habit modified")
            return redirect('habits:habit')
    else:
        form = HabitForm(instance=habit)
    return redirect('habits:habit')


def delete_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id)
        habit.delete()
        messages.success(request, "habit eliminated")

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
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']


            HabitEvent.objects.create(
                habit=habit,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,

            )
            messages.success(request, "Event Created.")
            
    return redirect('habits:index')


def edit_habit_event(request, habit_event_id):
    habit_event = get_object_or_404(HabitEvent, pk=habit_event_id)  
    if request.method == 'POST':
        form = HabitEventForm(request.POST, instance=habit_event)  
        if form.is_valid():
            form.save() 
            messages.success(request, "Event Modified.") 
            return redirect('habits:index')
    else:
        form = HabitEventForm(instance=habit_event)
    return redirect('habits:index')


def delete_habit_event(request, habit_event_id):
    if request.method == 'POST':
        habit_event = get_object_or_404(HabitEvent, id=habit_event_id)
        habit_event.delete()
        messages.success(request, "Event Eliminated")

    return redirect('habits:index')


