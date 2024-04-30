from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from general_app.views import is_teacher
from .models import TeacherInfo
from students_app.models import StudentInfo, DailySchoolFees
from payment_app.forms import DailyPaymentForm
# Create your views here.

"""
Renders the teacher homepage view.

This view is responsible for rendering the teacher homepage template, 'teacher_homepage.html', with the appropriate context data.
"""
@user_passes_test(is_teacher)
def teacher_homepage_view(request):
    teacherdata = TeacherInfo.objects.filter(
        status=True, user_id=request.user.id
    )
    context = {
        'name': teacherdata[0].get_name,
        'salary': teacherdata[0].salary,
        'joindate': teacherdata[0].joindate,
        'mobile': teacherdata[0].mobile,
    }
    return render(request, 'teacher_homepage.html', context)

@user_passes_test(is_teacher)
def teacher_students_to_pay_view(request):
    students = StudentInfo.objects.filter(status=True, checkifpaiddaily=False)

    context = {
        'students': students,
    }
    return render(request, 'students/daily_payments/teacher_students_to_pay.html', context)

@user_passes_test(is_teacher)
def teacher_student_daily_payment_view(request, pk):
    daily_school_fees = DailySchoolFees.objects.last().amount
    student = StudentInfo.objects.get(id=pk)
    payment_form = DailyPaymentForm(initial={'student': student})
    student_previous_payments = student.payment_set.all()
    if request.method == 'POST':
        payment_form = DailyPaymentForm(request.POST)
        if payment_form.is_valid():
            debt = payment_form.cleaned_data['debt']
            balance = payment_form.cleaned_data['balance']
            student.daily_balance = balance
            student.checkifpaiddaily = True
            student.save()
            payment_form.save()
            return redirect('teacher_students_to_pay')
    context = {
        'student': student,
        'payment_form': payment_form,
        'student_previous_payments': student_previous_payments,
        'daily_school_fees': daily_school_fees,
    }
    return render(request, 'students/daily_payments/teacher_student_daily_payment.html', context)


