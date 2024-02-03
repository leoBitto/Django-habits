# File: habits/utils.py
import plotly.express as px
import numpy as np
from django.db.models import Q
from .forms import ReportForm
from .models import Habit, HabitEvent
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.graph_objs as go
import plotly.io as pio


def convert_time_to_minutes(time):
    """
    Convert datetime.time object to minutes from midnight.
    """
    return time.hour * 60 + time.minute


def generate_heat_map(start_date, end_date):
    """
    Generate a heatmap of correlations between habits based on event times.

    Parameters:
    - start_date: Start date for extracting habit events.
    - end_date: End date for extracting habit events.

    Returns:
    - Success flag: Boolean indicating whether the generation was successful.
    - heatmap_html: HTML of the heatmap chart.
    """
    try:
        # Extract habit events and their times
        events_data = HabitEvent.objects.filter(
            Q(date__gte=start_date) & Q(date__lte=end_date)
        ).values('habit__name', 'time').order_by('habit__name', 'time')

        df = pd.DataFrame.from_records(events_data)

        df.dropna(inplace=True)

        # Calcola i minuti da mezzanotte direttamente dalla colonna 'time'
        df['minutes_from_midnight'] = df['time'].apply(lambda x: x.hour * 60 + x.minute)

        habit_names = df['habit__name'].unique()
        correlation_values = []

        for habit1 in habit_names:
            row = []
            for habit2 in habit_names:
                habit1_events = df[df['habit__name'] == habit1]['minutes_from_midnight']
                habit2_events = df[df['habit__name'] == habit2]['minutes_from_midnight']
                min_length = min(len(habit1_events), len(habit2_events))
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

        return True, heatmap_html

    except Exception as e:
        return False, f"Error generating heatmap: {str(e)}"

def generate_pie_chart(start_date, end_date):
    """
    Generate a pie chart showing the positivity ratio of habit events.

    Parameters:
    - start_date: Start date for extracting habit events.
    - end_date: End date for extracting habit events.

    Returns:
    - Success flag: Boolean indicating whether the generation was successful.
    - pie_chart_html: HTML of the pie chart.
    """
    try:
        events = HabitEvent.objects.filter(
            Q(date__gte=start_date) & Q(date__lte=end_date)
        )

        total_events = events.count()
        positive_events = events.filter(habit__is_positive=True).count()

        if total_events > 0:
            positivity_ratio = positive_events / total_events
        else:
            positivity_ratio = 0

        data_for_pie_chart = {
            'Labels': ['Positive', 'Negative'],
            'Values': [positivity_ratio, 1 - positivity_ratio],
        }

        fig = px.pie(
            data_for_pie_chart,
            values='Values',
            names='Labels',
            hole=0.6,
            color='Labels',
            color_discrete_map={'Positive': '#032cfc', 'Negative': '#fc0303'},
        )

        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0.05))

        pie_chart_html = fig.to_html(full_html=False)

        return True, pie_chart_html

    except Exception as e:
        return False, f"Error generating pie chart: {str(e)}"

def generate_daily_chart(start_date, end_date, habit_id):
    """
    Generate a line chart showing daily occurrences of a specific habit.

    Parameters:
    - start_date: Start date for extracting habit events.
    - end_date: End date for extracting habit events.
    - habit_id: ID of the habit for which the chart is generated.

    Returns:
    - Success flag: Boolean indicating whether the generation was successful.
    - daily_html: HTML of the daily chart.
    """
    try:
        habit = Habit.objects.get(pk=habit_id)
        habit_events = habit.habitevent_set.filter(date__range=(start_date, end_date)).values()

        df = pd.DataFrame().from_records(
            habit_events, 
            columns=['date', 'time']
        )
        
        df = df.groupby(by=["date"], as_index=False).count()

        date_range = pd.date_range(start=start_date, end=end_date)
        df_dates = pd.DataFrame(date_range, columns=['date'])
        df['date'] = pd.to_datetime(df['date'])
        df = pd.merge(df_dates, df, how='left', on='date')

        df = df.fillna(0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df['time'],
                                mode='lines',
                                name=habit.name,
                                line=dict(color='black'),))
        fig.update_layout(
            margin=dict(l=5, r=5, b=5, t=10, pad=2),
            yaxis=dict(
                title=dict(text="", font=dict(size=16, color='#000000')),
                range=[0, max(df['time']) + 3]
            ),
            paper_bgcolor="#FFD180",
            plot_bgcolor="#FFD180",
        )
        
        daily_html = fig.to_html(full_html=False)

        return True, daily_html

    except Exception as e:
        return False, f"Error generating daily chart: {str(e)}"

def generate_hourly_chart(start_date, end_date, habit_id):
    """
    Generate a bar chart showing hourly occurrences of a specific habit.

    Parameters:
    - start_date: Start date for extracting habit events.
    - end_date: End date for extracting habit events.
    - habit_id: ID of the habit for which the chart is generated.

    Returns:
    - Success flag: Boolean indicating whether the generation was successful.
    - hourly_html: HTML of the hourly chart.
    """
    try:
        habit = Habit.objects.get(pk=habit_id)
        habit_events = habit.habitevent_set.filter(date__range=(start_date, end_date)).values()

        df = pd.DataFrame().from_records(
            habit_events, 
            columns=['date','time']
        )
        df.dropna(inplace=True)
        df['hour'] = df['time'].apply(lambda x: x.hour)
        df = df.groupby(by=["hour"], as_index=False).count()
        hours_range = list(range(24))
        df_hours = pd.DataFrame(hours_range, columns=['hour'])
        df = pd.merge(df_hours, df, how='left', on='hour')
        df = df.fillna(0)

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
            margin=dict(l=5, r=5, b=5, t=10, pad=2),
            yaxis=dict(
                title=dict(text="", font=dict(size=16, color='#000000')),
                range=[0, max(df['time']) + 3]
            ),
            paper_bgcolor="#FFD180",
            plot_bgcolor="#FFD180",
        )
        
        hourly_html = fig.to_html(full_html=False)

        return True, hourly_html

    except Exception as e:
        return False, f"Error generating hourly chart: {str(e)}"
