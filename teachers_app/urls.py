from django.urls import path
from .views import teacher_students_to_pay_view, teacher_student_daily_payment_view

urlpatterns = [
    path('students-to-pay', teacher_students_to_pay_view, name='teacher_students_to_pay'),
    path('student-<str:pk>-daily-fee', teacher_student_daily_payment_view, name='teacher_student_daily_payment'),
]
