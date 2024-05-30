from django.db import models
from students_app.models import StudentInfo


class SchoolFeesPayment(models.Model):
    student = models.ForeignKey(
        StudentInfo, null=True, on_delete=models.SET_NULL)
    school_fees = models.FloatField(null=True)
    date = models.DateField(blank=True, null=True)
    debt = models.FloatField(null=True)
    troll = models.BooleanField(default=False)
    soap = models.BooleanField(default=False)
    broom = models.BooleanField(default=False)

