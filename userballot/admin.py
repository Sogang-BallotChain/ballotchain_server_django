from django.contrib import admin
from . import models
# Register your models here.

class UserBallotAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'ballot']

class UserBallotRegisterAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'ballot']
   
admin.site.register(models.UserBallot, UserBallotAdmin)
admin.site.register(models.UserBallotRegister, UserBallotRegisterAdmin)
