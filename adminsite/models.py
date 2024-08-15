from django.db import models

# Create your models here.


class Event(models.Model):
    sportsname = models.CharField( max_length=50)
    teamA = models.CharField( max_length=50)
    teamB = models.CharField( max_length=50)
    eventdate = models.DateField()
    eventtime = models.TimeField()
    description = models.TextField()
    betprice = models.IntegerField()
