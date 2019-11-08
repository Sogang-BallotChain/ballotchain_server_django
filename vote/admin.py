from django.contrib import admin
# Register your models here.
from . import models

class BallotAdmin (admin.ModelAdmin):
    list_display = ['id', 'candidate_list', 'start_time', 'end_time']

admin.site.register(models.Ballot, BallotAdmin)

