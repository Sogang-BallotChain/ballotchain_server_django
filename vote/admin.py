from django.contrib import admin
# Register your models here.
from . import models

class BallotAdmin (admin.ModelAdmin):
    list_display = ['id', 'name', 'candidate_list', 'start_time', 'end_time', 'address']

admin.site.register(models.Ballot, BallotAdmin)

