from notice_app.models import Notice
from django import forms


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['by', 'message']
