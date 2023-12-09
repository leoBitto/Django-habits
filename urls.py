# habits/urls.py
# path('habits/', include('habits.urls', namespace='habits')),
from django.urls import path
from . import views

app_name = 'habits'
urlpatterns = [
    # Visualizzazione del overviews
    path('overview/', views.overview, name='overview'),
    path('show_graph/<int:habit_id>', views.show_graph, name="show_graph"),

    #visualizzazione calendario
    path('calendar/<int:year>/<int:month>/', views.calendar, name='calendar'),
    path('day/<int:year>/<int:month>/<int:day>/', views.day, name='day'),

    # Gestione delle categorie
    path('categories/', views.category, name='category'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    # Gestione delle abitudini
    path('habits/', views.habit, name='habit'),
    path('habits/create/', views.create_habit, name='create_habit'),
    path('habits/<int:habit_id>/edit/', views.edit_habit, name='edit_habit'),
    path('habits/<int:habit_id>/delete/', views.delete_habit, name='delete_habit'),

    # Gestione degli eventi
    path('habit_events/', views.habit_event, name='habit_event'),
    path('habit_events/create/', views.create_habit_event, name='create_habit_event'),
    path('habit_events/<int:habit_event_id>/edit/', views.edit_habit_event, name='edit_habit_event'),
    path('habit_events/<int:habit_event_id>/delete/', views.delete_habit_event, name='delete_habit_event'),

]
