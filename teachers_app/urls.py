from django.urls import path
from .views import teacher_students_to_pay_view

urlpatterns = [
    path('students-to-pay', teacher_students_to_pay_view, name='teacher_students_to_pay'),

]
