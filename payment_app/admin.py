from django.contrib import admin
from .models import Payment, DailySchoolFees

# Register your models here.
admin.site.register(Payment)
admin.site.register(DailySchoolFees)
