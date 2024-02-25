from django.db import models

# Create your models here.
class Town(models.Model):
    name = models.CharField(max_length=255)
    lorry_fair = models.FloatField(default=0)

    def __str__(self):
        return self.name

