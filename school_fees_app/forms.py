from django import forms
from .models import SchoolFeesPayment
import datetime


class TermlyPaymentForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = SchoolFeesPayment
        fields = ['student', 'school_fees', 'date',
                  'debt', 'troll', 'soap', 'broom']
