# File: habits/utils.py

from calendar import HTMLCalendar
from django.urls import reverse

class Calendar(HTMLCalendar):
    def __init__(self, items=None, year=None, month=None):
        self.items = items or []
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day):
        d = ''
        for item in self.items:
            if item.start_time.day == day:
                d += f'<li class="calendar_list"> {item.get_html_url()} </li>'

        if day != 0:
            day_url = reverse('day', kwargs={'year': self.year, 'month': self.month, 'day': day})
            return f"<td><a href='{day_url}'><span class='date'>{day}</span></a><ul> {d} </ul></td>"

        return '<td></td>'

    def formatweek(self, theweek):
        week = ''
        for d, _ in theweek:
            week += self.formatday(d)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal
