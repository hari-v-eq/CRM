from calendar import HTMLCalendar, weekday
from turtle import title
from .models import *
from django.shortcuts import render
from datetime import date
from .models import Event



class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, title=None ):
		self.year = year
		self.month = month
		self.title = title
		
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		# events_per_day = events.filter(start_time__day=day)
		events_per_day = events.filter(start_time__day__gte=day, end_time__day__lte=day)
		d = ''
		
		for event in events_per_day:
			
			d += f'<li> {event.get_html_url} </li>'
			print(".......................",event)

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'
 

	# formats a week as a tr	
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		# events=Event.objects.all()
		print("++++++++++++++++",events)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		
		for week in self.monthdays2calendar(self.year, self.month):
				
				cal += f'{self.formatweek(week, events)}\n'
			
		return cal