from django.db import models
from user.models import User
from vote.models import Ballot
# Create your models here.

class UserBallot (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)