from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from general_app.views import is_teacher
from .models import TeacherInfo
from students_app.models import StudentInfo, DailySchoolFees
from payment_app.forms import DailyPaymentForm
from payment_app.models import Payment
from notice_app.models import Notice
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
    payments = Payment.objects.filter(user=request.user)
    notices = Notice.objects.all()
    context = {
        'name': teacherdata[0].get_name,
        'salary': teacherdata[0].salary,
        'joindate': teacherdata[0].joindate,
        'mobile': teacherdata[0].mobile,
        'payments': payments,
        'notices': notices,
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
    student = get_object_or_404(StudentInfo, pk=pk)
    payment_form = DailyPaymentForm()
    student_previous_payments = student.payment_set.all()

    if request.method == 'POST':
        payment_form = DailyPaymentForm(request.POST)
        if payment_form.is_valid():
            debt = payment_form.cleaned_data['debt']
            balance = payment_form.cleaned_data['balance']
            student.daily_debt = debt
            student.daily_balance = balance
            student.checkifpaiddaily = True
            student.save()
            user = request.user
            payment = payment_form.save(commit=False)
            payment.student = student
            payment.user = user
            payment.save()
            return redirect('teacher_students_to_pay')
    context = {
        'student': student,
        'payment_form': payment_form,
        'student_previous_payments': student_previous_payments,
        'daily_school_fees': daily_school_fees,
    }
    return render(request, 'students/daily_payments/teacher_student_daily_payment.html', context)

@user_passes_test(is_teacher)
def teacher_daily_paid_students_view(request):
    students = StudentInfo.objects.filter(status=True, checkifpaiddaily=True)
    student_last_payments = {}
    
    for student in students:
        last_payment = Payment.objects.filter(student=student, user=request.user).last()
        student_last_payments[student] = last_payment
    context = {
        'student_last_payments': student_last_payments,
    }
    return render(request, 'students/daily_payments/teacher_daily_paid_students.html', context)

@user_passes_test(is_teacher)
def teacher_delete_daily_paid_student_view(request, pk):
    students_paid = StudentInfo.objects.get(id=pk)
    last_payment = Payment.objects.filter(student=students_paid)
    delete_last = last_payment.last()
    if request.method == 'POST':
        delete_last.delete()
        students_paid.checkifpaiddaily = False
        students_paid.save()

    return redirect('teacher_daily_paid_students')

@user_passes_test(is_teacher)
def teacher_students_payment_records_view(request):
    payments = Payment.objects.filter(user=request.user)

    context = {
        'payments': payments
    }
    return render(request, 'students/records/teacher_students_payment_records.html', context)