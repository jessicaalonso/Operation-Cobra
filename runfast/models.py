from django.db import models

class Workout(models.Model):
	userid = models.PositiveIntegerField()
	distance = models.DecimalField(max_digits=4, decimal_places=2)
	date = models.DateField()
 	duration = models.PositiveIntegerField(blank=True, null=True)
 	hours = models.PositiveIntegerField(blank=True, null=True)
 	minutes = models.PositiveIntegerField(blank=True, null=True)
 	seconds = models.PositiveIntegerField(blank=True, null=True)
 	road = models.NullBooleanField(blank=True, null=True)
 	trail = models.NullBooleanField(blank=True, null=True)
	interval = models.NullBooleanField(blank=True, null=True)
	treadmill = models.NullBooleanField(blank=True, null=True)
	longrun = models.NullBooleanField(blank=True, null=True)
	hills = models.NullBooleanField(blank=True, null=True)
	temporun = models.NullBooleanField(blank=True, null=True)
	newshoes = models.NullBooleanField(blank=True, null=True)
	
#	def __unicode__(self):
#		return self.id

	class Meta:
		ordering = ['date']
		
class Races(models.Model):
	racename = models.CharField(max_length=100)
	raceday = models.DateField()
	racedistance = models.DecimalField(max_digits=4, decimal_places=2)
#	goaltime = 

	def __unicode__(self):
		return self.racename