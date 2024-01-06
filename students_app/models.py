from django.db import models
from django.contrib.auth.models import User
from admin_app.models import Town, Classroom
from payment_app.models import PAYMENT_CATEGORY, PAYMENT_METHOD, FORM_OF_TRANSPORTATION

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

class StudentInfo(models.Model):
    roll = models.CharField(max_length=40)
    date_of_admission = models.DateField(null=True, blank=True)
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=45, default='', blank=True, choices=GENDER)
    mother = models.CharField(max_length=45, default='', blank=True)
    father = models.CharField(max_length=45, default='', blank=True)
    mobile = models.CharField(max_length=40, default='', blank=True)
    cl = models.OneToOneField(Classroom, default='', on_delete=models.CASCADE)
    residence = models.OneToOneField(Town, default='', on_delete=models.CASCADE)
    fee = models.FloatField(null=True, default=210)
    foodfee = models.FloatField(null=True, blank=True)
    carfee = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False)
    checkifpaiddaily = models.BooleanField(default=False)
    checkifpaidterm = models.BooleanField(default=False)
    daily_debt = models.FloatField(null=True, blank=True, default=0)
    daily_balance = models.FloatField(null=True, blank=True, default=0)
    termly_debt = models.FloatField(null=True, blank=True)
    payment_category = models.CharField(
        max_length=40, choices=PAYMENT_CATEGORY, blank=True)
    form_of_transportation = models.CharField(
        max_length=40, choices=FORM_OF_TRANSPORTATION, blank=True)
    payment_method = models.CharField(
        max_length=40, choices=PAYMENT_METHOD, blank=True)
    troll = models.BooleanField(default=False)
    soap = models.BooleanField(default=False)
    broom = models.BooleanField(default=False)

    passport = models.ImageField(
        blank=True, null=True, upload_to="static/images/passports/")
    
    
    @property
    def full_name(self):
        return self.user_profile.first_name+' '+self.user_profile.last_name
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if self._state.adding or self.payment_method == 'School_Fees_Aside':
            self.termly_debt = 210
        super(StudentInfo, self).save(*args, **kwargs)    