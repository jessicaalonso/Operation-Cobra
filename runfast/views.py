from django.shortcuts import render_to_response, get_object_or_404
from newdev.runfast.models import Workout, Races
import datetime, calendar
import re
import string
import decimal


##############################################################

def calendar_view(request):
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec'] 
	 
	today = datetime.datetime.date(datetime.datetime.now())
	 
	current = re.split('-', str(today))
	current_no = int(current[1])
	current_month = year[current_no-1]
	current_month = string.upper(current_month)
	current_day = int(re.sub('\A0', '', current[2]))
	current_yr = int(current[0])

	### modifies month and year if they click previous ###
	
	if request.method == 'POST':
		if 'earlier' in request.POST:
			displayed_date = request.POST['earlier']
			displayed_date = str(displayed_date)
			displayed_date = datetime.datetime.strptime(displayed_date, "%b. %d, %Y")
			if displayed_date.month == 1:
				current_no = 12
				current_yr = displayed_date.year - 1
			else:
				current_no = displayed_date.month - 1
				current_yr = displayed_date.year
		elif 'next' in request.POST:
			displayed_date = request.POST['next']
			displayed_date = str(displayed_date)
			displayed_date = datetime.datetime.strptime(displayed_date, "%b. %d, %Y")
			if displayed_date.month == 12:
				current_no = 1
				current_yr = displayed_date.year + 1
			else:
				current_no = displayed_date.month + 1
				current_yr = displayed_date.year

	### for submitting run entry ###
		elif 'view_date_on_submit' in request.POST:
			### this part sets the correct year and month for generating the calendar ###
			displayed_date = request.POST['view_date_on_submit']
			displayed_date = str(displayed_date)
			displayed_date = datetime.datetime.strptime(displayed_date, "%b. %d, %Y")
			current_no = displayed_date.month
			current_yr = displayed_date.year
	
			run_distance = request.POST['distance']
			run_distance = str(run_distance)
	
			run_date = request.POST['date']
			run_date = str(run_date)
			
			if request.POST['hours'] == 'hr':
				run_hours = 0
			elif request.POST['hours'] == '':
				run_hours = 0
			else:
				run_hours = request.POST['hours']
				run_hours = int(run_hours)
			
			if request.POST['minutes'] == 'min':
				run_minutes = 0
			elif request.POST['minutes'] == '': 
				run_minutes = 0			
			else:
				run_minutes = request.POST['minutes']
				run_minutes = int(run_minutes)
				
			if request.POST['seconds'] == 'sec':
				run_seconds = 0
			elif request.POST['seconds'] == '':
				run_seconds = 0
			else:
				run_seconds = request.POST['seconds']
				run_seconds = int(run_seconds)
				
			run_duration = run_seconds + (run_minutes * 60) + (run_hours * 60 * 60)
			
			if 'road' in request.POST:
				road = request.POST['road']
			else:	
				road = False
			
			if 'trail' in request.POST:
				trail = request.POST['trail']
			else:
				trail = False	
	
			if 'interval' in request.POST:		
				interval = request.POST['interval']
			else:	
				interval = False

			if 'treadmill' in request.POST:		
				treadmill = request.POST['treadmill']
			else:	
				treadmill = False
			
			if 'longrun' in request.POST:		
				longrun = request.POST['longrun']
			else:	
				longrun = False
			
			if 'hills' in request.POST:
				hills = request.POST['hills']
			else:	
				hills = False
			
			if 'tempo' in request.POST:
				temporun = request.POST['tempo']
			else:	
				temporun = False

			if 'newshoes' in request.POST:
				newshoes = request.POST['newshoes']
			else:	
				newshoes = False
	
			p= Workout(distance=run_distance, date=run_date, duration=run_duration, hours=run_hours, minutes=run_minutes , seconds=run_seconds, road=road, trail=trail, interval=interval, treadmill=treadmill, longrun=longrun, hills=hills, temporun=temporun, newshoes=newshoes)
			p.save()
			
		else:
			displayed_date = []			
	else:
		displayed_date = []
	
	month_cal = calendar.Calendar().monthdatescalendar(current_yr, current_no)
	nweeks = len(month_cal)
	
	month_cal_mod = []
	for week in month_cal:
		new_week = []
		for day in week:
			if Workout.objects.filter(date=day).exists():
				new_day = [day, Workout.objects.get(date=day)]
			else:
				new_day = [day, '']
			new_week.append(new_day)
		month_cal_mod.append(new_week)
		
	Racedb = Races.objects.all()
	
	return render_to_response('runfast/calendar_template.html', {'month_cal_mod': month_cal_mod, 'Workout': Workout, 'Racedb': Racedb,})


###########################################################
def run_detail_view(request):

	if request.method == 'POST':
		if 'requested_date' in request.POST:
			requested_date = request.POST['requested_date']
			run_to_detail = Workout.objects.get(date=requested_date)
		else:
			run_to_detail = ''	

	return render_to_response('runfast/run_detail_template.html', {'run_to_detail': run_to_detail})
	
############################################################
def analytics_view(request):
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	
	return render_to_response('runfast/analytics_template.html', {'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})
	
##########################################################

def pacebyweek_view(request):

	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	# generate calendar for selected months

	selected_year = 2012
	selected_month = 1
	month_cal = calendar.Calendar().monthdatescalendar(selected_year, selected_month)

	# dedupe overlapping weeks (when more than one month)

	# create list of week names ie "Jan 1 - Jan 7"
	week_name_list =[]
	week_speed_list = []
	for week in month_cal:
		start_month = week[0].month
		start_day = week[0].day
		end_month = week[6].month
		end_day = week[6].day
		week_name = '%s/%s - %s/%s' % (start_month, start_day, end_month, end_day)
		week_name_list.append(week_name)
		
		week_mileage = 0
		week_duration = 1
		for day in week:
			if Workout.objects.filter(date=day).exists():
				day_mileage = Workout.objects.get(date=day).distance
				week_mileage += day_mileage
				day_duration = Workout.objects.get(date=day).duration
				week_duration += day_duration
		week_speed = 60*60* week_mileage/(decimal.Decimal(week_duration))
		
		week_speed_list.append(str(week_speed))  
		
	xaxis_list = week_name_list
	yaxis_list = week_speed_list

	return render_to_response('runfast/pacebyweek_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})


###
def pacebymonth_view(request):
	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)

	# generate calendar for selected months
	
	# dedupe overlapping weeks (when more than one month)

	year_list = [2012]  # this is just hardwired in for now
	month_list = [1] # this is just hardwired in for now
	dbfilter = Workout.objects.filter(date__contains="2012-01")
	month_mileage = 0
	month_duration = 0
	for run in dbfilter:
		month_mileage += run.distance
		month_duration += run.duration
	month_speed = 3600*month_mileage/month_duration
	month_speed_list = [month_speed]
	
	xaxis_list = month_list
	yaxis_list = month_speed_list

	return render_to_response('runfast/pacebymonth_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})

###
def mileagebyweek_view(request):
	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	# generate calendar for selected months

	selected_year = 2012
	selected_month = 1
	month_cal = calendar.Calendar().monthdatescalendar(selected_year, selected_month)

	# dedupe overlapping weeks (when more than one month)

	# create list of week names ie "Jan 1 - Jan 7"
	week_name_list =[]
	week_mileage_list = []
	for week in month_cal:
		start_month = week[0].month
		start_day = week[0].day
		end_month = week[6].month
		end_day = week[6].day
		week_name = '%s/%s - %s/%s' % (start_month, start_day, end_month, end_day)
		week_name_list.append(week_name)
		
		week_mileage = 0
		for day in week:
			if Workout.objects.filter(date=day).exists():
				day_mileage = Workout.objects.get(date=day).distance
				week_mileage += day_mileage
		week_mileage_list.append(week_mileage)
		
	xaxis_list = week_name_list
	yaxis_list = week_mileage_list

	return render_to_response('runfast/mileagebyweek_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})


###
def mileagebymonth_view(request):
	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)

	# generate calendar for selected months
	
	# dedupe overlapping weeks (when more than one month)

	year_list = [2012]  # this is just hardwired in for now
	month_list = [1] # this is just hardwired in for now
	dbfilter = Workout.objects.filter(date__contains="2012-01")
	month_mileage = 0
	for run in dbfilter:
		month_mileage += run.distance
	month_mileage = [str(month_mileage), '']
	
	xaxis_list = month_list
	yaxis_list = month_mileage

	return render_to_response('runfast/mileagebymonth_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})



###
def mileagebyyear_view(request):
	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)
	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	
	year_list = [2012]  # this is just hardwired in for now
	dbfilter = Workout.objects.filter(date__contains="2012")
	year_mileage = 0
	for run in dbfilter:
		year_mileage += run.distance
	year_mileage = [str(year_mileage), '']
	
	xaxis_list = year_list
	yaxis_list = year_mileage
	
	return render_to_response('runfast/mileagebyyear_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})



#########	
def weeklymileageincrease_view(request):
	
# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	# generate calendar for selected months

	selected_year = 2012
	selected_month = 1
	month_cal = calendar.Calendar().monthdatescalendar(selected_year, selected_month)

	# dedupe overlapping weeks (when more than one month)

	# create list of week names ie "Jan 1 - Jan 7"
	week_name_list =[]
	week_mileage_list = []
	for week in month_cal:
		start_month = week[0].month
		start_day = week[0].day
		end_month = week[6].month
		end_day = week[6].day
		week_name = '%s/%s - %s/%s' % (start_month, start_day, end_month, end_day)
		week_name_list.append(week_name)
		
		week_mileage = 0
		for day in week:
			if Workout.objects.filter(date=day).exists():
				day_mileage = Workout.objects.get(date=day).distance
				week_mileage += day_mileage
		week_mileage_list.append(week_mileage)
	
	#convert ints to floats
	float_week_mileage_list = []
	for x in week_mileage_list:
		a = float(x)
		float_week_mileage_list.append(a)
	
	#calculate percentage increase
	
	percent_increase_list = []
	for x,y in enumerate(float_week_mileage_list):
		if x>0 and float_week_mileage_list[x] > 0:
			try:
				get_previous = float_week_mileage_list[x-1]
				current = float_week_mileage_list[x]
				percent_increase = 100*(current-get_previous)/get_previous
				percent_increase_list.append(percent_increase)
			except ZeroDivisionError:
				percent_increase = float(0)
				percent_increase_list.append(percent_increase)	
			
		else:	
			percent_increase = float(0)
			percent_increase_list.append(percent_increase)
	
	xaxis_list = week_name_list
	yaxis_list = percent_increase_list	
	
	return render_to_response('runfast/weeklymileageincrease_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})	



###
def monthlymileageincrease_view(request):
	return render_to_response('runfast/chart_template.html')
###
def longrunpercentofweek_view(request):
	# generate workout date selector
	year = ['Jan', 
	'Feb', 
	'Mar', 
	'Apr', 
	'May', 
	'June', 
	'Jul', 
	'Aug', 
	'Sept', 
	'Oct', 
	'Nov', 
	'Dec']
	
	workout_date_list = Workout.objects.order_by("date")
	workout_years = []
	for x in workout_date_list:
		years = x.date.year
		if years not in workout_years:
			workout_years.append(years)	
	
	workout_strip_day = []
	for x in workout_date_list:
		strip_day = [year[x.date.month-1], x.date.year]
		if strip_day not in workout_strip_day:
			workout_strip_day.append(strip_day)
	
	# generate calendar for selected months

	selected_year = 2012
	selected_month = 1
	month_cal = calendar.Calendar().monthdatescalendar(selected_year, selected_month)

	# dedupe overlapping weeks (when more than one month)

	# create list of week names ie "Jan 1 - Jan 7"
	week_name_list =[]
	week_longrun_percent_list = []
	for week in month_cal:
		start_month = week[0].month
		start_day = week[0].day
		end_month = week[6].month
		end_day = week[6].day
		week_name = '%s/%s - %s/%s' % (start_month, start_day, end_month, end_day)
		week_name_list.append(week_name)
		
		week_mileage = 0
		longest_run = 0
		for day in week:
			if Workout.objects.filter(date=day).exists():
				day_mileage = Workout.objects.get(date=day).distance
				week_mileage += day_mileage
				if day_mileage > longest_run:
					longest_run = day_mileage
		try:
			longrun_percent = 100 * longest_run/week_mileage
		except ZeroDivisionError:
			longrun_percent = 0
		
		week_longrun_percent_list.append(str(longrun_percent))
		
	xaxis_list = week_name_list
	yaxis_list = week_longrun_percent_list
	
	return render_to_response('runfast/longrun_percent_template.html', {'xaxis_list': xaxis_list, 'yaxis_list': yaxis_list, 'workout_years': workout_years, 'workout_strip_day': workout_strip_day,})


