# habits/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Category, Habit, HabitEvent, Goal
from .forms import *

def overview(request):
    categories = Category.objects.all()
    habits = Habit.objects.all()
    habit_events= HabitEvent.objects.all()
    goals = Goal.objects.all()



    context={
        
    }

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

        Category.objects.create(
            name=name,
            color=color,
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

    for habit in habits:
        edit_habit_form = HabitForm(instance=habit)
        habit_form_dict[habit] = edit_habit_form

    context = {
        'habits': habits,
        'habit_form': habit_form,
        'habit_form_dict': habit_form_dict,
    }

    return render(request, 'habits/habit.html', context)

def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            icon = form.cleaned_data['icon']

            Habit.objects.create(
                name=name,
                category=category,
                icon=icon
            )
    return redirect('habits:habit')

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


# goal views

def goal(request):

    context={
        
    }

    return render(request, 'habits/goal.html', context) 

def create_goal(request):
    pass

def edit_goal(request):
    pass

def delete_goal(request):
    pass

# habit event views

def habit_event(request):

    context={
    
    }

    return render(request, 'habits/habit_event.html', context) 

def create_habit_event(request):
    pass

def edit_habit_event(request):
    pass

def delete_habit_event(request):
    pass