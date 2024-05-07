from django import forms
from .models import Payment
import datetime


class DailyPaymentForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Payment
        fields = ['user', 'student', 'amount', 'bus_fee', 'school_fees',
                  'balance', 'debt', 'date',]
