from django.db import models

# Create your models here.
class Town(models.Model):
    town_name = models.CharField(max_length=50)
    bus_fee = models.FloatField(null=True)

    def __str__(self):
        return self.town_name
    
class Classroom(models.Model):
    class_name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.class_name    