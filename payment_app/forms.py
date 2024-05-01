from django import forms
from .models import Payment
import datetime


class DailyPaymentForm(forms.ModelForm):
    when_made = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Payment
        fields = ['user', 'student', 'pay', 'carpay', 'schoolfees',
                  'balance', 'debt', 'when_made',]
