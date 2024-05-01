from django.db import models
from students_app.models import StudentInfo
from django.contrib.auth.models import User

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(
        StudentInfo, null=True, on_delete=models.SET_NULL, blank=True)
    pay = models.FloatField(null=True, blank=True, default=0)
    carpay = models.FloatField(null=True, blank=True, default=0)
    schoolfees = models.FloatField(null=True, blank=True, default=0)
    when_made = models.DateField(blank=True, null=True)
    balance = models.FloatField(null=True)
    debt = models.FloatField(null=True)



