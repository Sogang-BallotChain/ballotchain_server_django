from django.db import models

# Create your models here.

class User (models.Model):
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    eth_pub_key = models.CharField(max_length=42)
    eth_prv_key = models.CharField(max_length=42)