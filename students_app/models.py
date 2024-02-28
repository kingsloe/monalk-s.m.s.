from django.db import models
from django.contrib.auth.models import User
from general_app.models import Town

# Create your models here.
GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

CLASSES = [
    ('F & B', 'F & B'),
    ('P.S.', 'P.S.'),
    ('K.S.A.', 'K.S.A.'),
    ('K.S.B.', 'K.S.B.'),
    ('K.S.C.', 'K.S.C.'),
    ('L.S.A.', 'L.S.A.'),
    ('L.S.B.', 'L.S.B.'),
    ('L.S.C.', 'L.S.C.')
]

FORM_OF_TRANSPORTATION = [
    ('Bus', 'Bus'),
    ('Walk', 'Walk')
]

PAYMENT_METHOD = [
    ('Pay_Per_Day', 'Pay Per Day'),
    ('School_Fees_Aside', 'School Fees Aside')

]

PAYMENT_CATEGORY = [
    ('Pay_Everything', 'Pay Everything'),
    ('Dont_Pay', 'Don\'t Pay'),
    ('Considered', 'Considered'),
]

class DailySchoolFees(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class StudentInfo(models.Model):
    class Meta:
        verbose_name_plural = 'Student Info'

    roll = models.CharField(max_length=10)
    date_of_admission = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=45, choices=GENDER)
    mother = models.CharField(max_length=100, blank=True)
    father = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=40, blank=True)
    grade = models.CharField(max_length=100, choices=CLASSES)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    fee = models.FloatField(null=True, default=210)
    foodfee = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False)
    checkifpaiddaily = models.BooleanField(default=False)
    checkifpaidterm = models.BooleanField(default=False)
    daily_debt = models.FloatField(null=True, blank=True, default=0)
    daily_balance = models.FloatField(null=True, blank=True, default=0)
    termly_debt = models.FloatField(null=True, blank=True, default=210)
    payment_category = models.CharField(
        max_length=40, choices=PAYMENT_CATEGORY)
    form_of_transportation = models.CharField(
        max_length=40, choices=FORM_OF_TRANSPORTATION)
    payment_method = models.CharField(
        max_length=40, choices=PAYMENT_METHOD)
    troll = models.BooleanField(default=False)
    soap = models.BooleanField(default=False)
    broom = models.BooleanField(default=False)

    passport = models.ImageField(
        blank=True, null=True, upload_to="static/images/passports/")

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

    def get_school_fees_aside_base_fee(self, base_fee, base_lorry_fair):
        if self.form_of_transportation == 'Walk':
            return 210
        elif self.form_of_transportation == 'Bus' and self.payment_category == 'Considered':
            return base_fee - (0.5 if self.town.name == 'Adamsu' else 1)
        return base_fee

    def get_pay_per_day_base_fee(self, base_fee, base_school_fee):
        if self.form_of_transportation == 'Walk':
            return base_school_fee - (0.5 if self.payment_category == 'Considered' else 0)
        elif self.form_of_transportation == 'Bus' and self.payment_category == 'Considered':
            return base_fee - (0.5 if self.payment_category == 'Considered'and self.town.name == 'Adamsu' else 1)
        return base_fee    


    def get_base_fee_components(self):
        base_school_fee = DailySchoolFees.objects.last().amount
        town = Town.objects.get(id=self.town_id)
        base_lorry_fair = town.lorry_fair
        return base_school_fee, base_lorry_fair

    def get_base_fee(self):
        base_school_fee, base_lorry_fair = self.get_base_fee_components()
        base_fee = base_school_fee + base_lorry_fair

        if self.payment_method == 'School_Fees_Aside':
            return self.get_school_fees_aside_base_fee(base_fee, base_lorry_fair)
        elif self.payment_method == 'Pay_Per_Day':
            return self.get_pay_per_day_base_fee(base_fee, base_school_fee)   


        
