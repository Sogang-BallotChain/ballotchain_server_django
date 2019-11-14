from django.contrib import admin

# Register your models here.
from . import models

class UserAdmin (admin.ModelAdmin):
    list_display = ['id', 'email', 'password', 'eth_pub_key']

admin.site.register(models.User, UserAdmin)