from django.urls import path
from .views import (teacher_students_to_pay_view, 
                    teacher_student_daily_payment_view, 
                    teacher_daily_paid_students_view,
                    teacher_delete_daily_paid_student_view,
                    teacher_students_payment_records_view,)

urlpatterns = [
    path('students-to-pay', teacher_students_to_pay_view, name='teacher_students_to_pay'),
    path('student-<str:pk>-daily-fee', teacher_student_daily_payment_view, name='teacher_student_daily_payment'),
    path('students-paid-recently', teacher_daily_paid_students_view, name='teacher_daily_paid_students'),
    path('delete-payment-<str:pk>', teacher_delete_daily_paid_student_view, name='teacher_delete_daily_paid_student'),
    path('payment-records', teacher_students_payment_records_view, name='teacher_students_payment_records'),
]
