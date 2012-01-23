from django.contrib import admin
from newdev.runfast.models import Races

class RaceAdmin(admin.ModelAdmin):
    list_display = ('racename')


admin.site.register(Races, RaceAdmin)
