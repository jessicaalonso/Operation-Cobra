from django.conf.urls.defaults import patterns, include, url
from newdev.runfast.views import calendar_view, run_detail_view, analytics_view, pacebyweek_view, pacebymonth_view, mileagebyweek_view, mileagebymonth_view, mileagebyyear_view, weeklymileageincrease_view, monthlymileageincrease_view, longrunpercentofweek_view

urlpatterns = patterns('',
	('^runfast/$', calendar_view),
	('^runfast/calendar/$', calendar_view),
	('^runfast/run_detail/$', run_detail_view),	
	('^runfast/analytics/$', mileagebyweek_view),
	
	
### graphs ###
	('^runfast/analytics/performance/pacebyweek/$', pacebyweek_view),
	('^runfast/analytics/performance/pacebymonth/$', pacebymonth_view),

	('^runfast/analytics/distance/mileagebyweek/$', mileagebyweek_view),
	('^runfast/analytics/distance/mileagebymonth/$', mileagebymonth_view),	
	('^runfast/analytics/distance/mileagebyyear/$', mileagebyyear_view),
	
	('^runfast/analytics/injuryprevention/weeklymileageincrease/$', weeklymileageincrease_view),
	('^runfast/analytics/injuryprevention/monthlymileageincrease/$', monthlymileageincrease_view),	
	('^runfast/analytics/injuryprevention/longrunpercentofweek/$', longrunpercentofweek_view),
	

		
)




from django.conf import settings
from newdev import settings
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)