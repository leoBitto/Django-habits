# File: habits/utils.py
import plotly.express as px
import numpy as np
from django.db.models import Q
from .forms import *
from .models import Category, Habit, HabitEvent
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.graph_objs as go
import plotly.io as pio

def convert_time_to_minutes(time):
    """
    Converte l'oggetto datetime.time in minuti dalla mezzanotte.
    """
    return time.hour * 60 + time.minute

def generate_heat_map(start_date, end_date):
    """
    Crea un grafico heatmap delle correlazioni tra abitudini basato sugli orari degli eventi.
    
    Parameters:
    - df: DataFrame contenente gli orari degli eventi delle abitudini
    
    Returns:
    - heatmap_html: HTML del grafico heatmap
    """
    
    # Estrai gli eventi e i relativi orari
    events_data = HabitEvent.objects.filter(
        Q(date__gte=start_date) & Q(date__lte=end_date)
    ).values('habit__name', 'date', 'time').order_by('habit__name', 'date', 'time')


    df = pd.DataFrame.from_records(events_data)

    # Modifica il tipo degli orari se sono di tipo datetime.time
    df['time'] = df['time'].apply(convert_time_to_minutes)

    habit_names = df['habit__name'].unique()
    correlation_values = []

    for habit1 in habit_names:
        row = []
        for habit2 in habit_names:
            habit1_events = df[df['habit__name'] == habit1]['time']
            habit2_events = df[df['habit__name'] == habit2]['time']
            # Trova la lunghezza minima tra le due liste
            min_length = min(len(habit1_events), len(habit2_events))
            
            # Considera solo i primi N valori della lista più lunga
            N = min_length
            habit1_events = habit1_events[:N]
            habit2_events = habit2_events[:N]
            correlation = np.corrcoef(habit1_events, habit2_events)[0, 1]
            row.append(correlation)
        correlation_values.append(row)


    heatmap_df = pd.DataFrame(correlation_values, index=habit_names, columns=habit_names)
    
    fig = px.imshow(heatmap_df,
                    labels=dict(color='Correlation'),
                    color_continuous_scale='Viridis',
                    )
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig.update_coloraxes(colorbar=dict(orientation="h", yanchor="bottom", title=None))
    heatmap_html = fig.to_html(full_html=False)

    return heatmap_html

def generate_pie_chart(start_date, end_date):

    events = HabitEvent.objects.filter(
        Q(date__gte=start_date) & Q(date__lte=end_date)
    )
    
    total_events = events.count()
    positive_events = events.filter(habit__is_positive=True).count()

    # Calcola la proporzione
    if total_events > 0:
        positivity_ratio = positive_events / total_events
    else:
        positivity_ratio = 0
    # Crea un dizionario con i dati per il grafico
    data_for_pie_chart = {
        'Labels': ['Positive', 'Negative'],
        'Values': [positivity_ratio, 1 - positivity_ratio],
    }

    # Utilizza Plotly per creare il grafico a torta
    fig = px.pie(
        data_for_pie_chart,
        values='Values',
        names='Labels',
        hole=0.6,
        color='Labels',
        color_discrete_map={'Positive': '#032cfc', 'Negative': '#fc0303'},
    )

    # Imposta la posizione della legenda sopra il grafico
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0.05))

    # Converte il grafico Plotly in HTML
    pie_chart_html = fig.to_html(full_html=False)
    
    return pie_chart_html

def generate_daily_chart(start_date, end_date, habit_id):

    # filtra gli eventi dell'abitudine per le date
    habit = Habit.objects.get(pk=habit_id)
    habit_events = habit.habitevent_set.filter(date__range=(start_date, end_date)).values()
    

    # crea il dataframe
    df = pd.DataFrame().from_records(
        habit_events, 
        columns=[
            'date',
            'time',
         ])
    
    
    df = df.groupby(by=["date"], as_index=False).count()

    # crea un DataFrame con tutte le date da start_date a end_date
    date_range = pd.date_range(start=start_date, end=end_date)
    df_dates = pd.DataFrame(date_range, columns=['date'])
    # converti la colonna 'date' in df in datetime
    df['date'] = pd.to_datetime(df['date'])
    # unisci df_dates con il tuo DataFrame originale
    df = pd.merge(df_dates, df, how='left', on='date')

    # riempi i valori mancanti
    df = df.fillna(0)
    
    #crea il grafico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df['time'],
                        mode='lines',
                        name=habit.name,
                        line=dict(color='black'),))
    fig.update_layout(
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=10,
            pad=2
        ),
        yaxis=dict(
            title=dict(text="", font=dict(size=16, color='#000000')),
            range=[0, max(df['time'])+3]  # Imposta l'intervallo dell'asse y per iniziare da 0
        ),
        paper_bgcolor="#FFD180",
        plot_bgcolor="#FFD180",
    )
        # Converte il grafico Plotly in HTML
    daily_html = fig.to_html(full_html=False)
    
    return daily_html

def generate_hourly_chart(start_date, end_date, habit_id):

    # filtra gli eventi dell'abitudine per le date
    habit = Habit.objects.get(pk=habit_id)
    habit_events = habit.habitevent_set.filter(date__range=(start_date, end_date)).values()
    

    # crea il dataframe
    df = pd.DataFrame().from_records(
        habit_events, 
        columns=['date','time']
        )

    # Estrai l'ora dalla colonna 'time'
    df['hour'] = df['time'].apply(lambda x: x.hour)
    # raggruppa per ora e conta le occorrenze
    df = df.groupby(by=["hour"], as_index=False).count()
    # crea un DataFrame con tutte le ore della giornata
    hours_range = list(range(24))
    df_hours = pd.DataFrame(hours_range, columns=['hour'])

    # unisci df_hours con il tuo DataFrame originale
    df = pd.merge(df_hours, df, how='left', on='hour')

    # riempi i valori mancanti
    df = df.fillna(0)

    #crea il grafico
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df['hour'], 
            y=df['time'],
            name=habit.name, 
            marker=dict(color='black')
            )
        )
    fig.update_layout(
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=10,
            pad=2
        ),
        yaxis=dict(
            title=dict(text="", font=dict(size=16, color='#000000')),
            range=[0, max(df['time'])+3]  # Imposta l'intervallo dell'asse y per iniziare da 0
        ),
        paper_bgcolor="#FFD180",
        plot_bgcolor="#FFD180",
    )
        # Converte il grafico Plotly in HTML
    daily_html = fig.to_html(full_html=False)
    
    return daily_html







