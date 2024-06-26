from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NoticeForm
from django.db.models import F
from django.forms.utils import ErrorList
import logging
from django.http import JsonResponse
from django.contrib.auth.models import Group

# |||||| IMPORTING FUNCTIONS FROM OTHER APPS ||||||||||
from general_app.views import is_admin
# |||||| IMPORTING FUNCTIONS FROM OTHER APPS ||||||||||


# |||||| IMPORTING FORMS FROM OTHER APPS ||||||||||
from teachers_app.forms import TeacherUserInfoForm, TeacherInfoForm
from students_app.forms import StudentUserInfoForm, StudentInfoForm
from school_fees_app.forms import TermlyPaymentForm
from payment_app.forms import DailyPaymentForm
# |||||| IMPORTING FORMS FROM OTHER APPS ||||||||||

# |||||| IMPORTING MODELS FROM OTHER APPS ||||||||||
from teachers_app.models import TeacherInfo, User
from students_app.models import StudentInfo, DailySchoolFees
from notice_app.models import Notice
from payment_app.models import Payment
from school_fees_app.models import SchoolFeesPayment
# |||||| IMPORTING MODELS FROM OTHER APPS ||||||||||


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_homepage_view(request):
    #Get the number of active and pending teachers and students
    active_teachers = TeacherInfo.objects.filter(status=True)
    pending_teachers = TeacherInfo.objects.filter(status=False)
    active_students = StudentInfo.objects.filter(status=True)
    pending_students = StudentInfo.objects.filter(status=False)

    # Get the sum of salaries of active teachers and the total fees of students
    teachers_salary = active_teachers.aggregate(Sum('salary'))['salary__sum']
    students_fees = active_students.count() * 210

    # Get all the notices
    notices = Notice.objects.all()

    # Creating dictionary with the variables to be passed to the template
    context = {
        'active_teachers': active_teachers.count(),
        'pending_teachers': pending_teachers.count(),
        'active_students': active_students.count(),
        'pending_students': pending_students.count(),
        'teachers_salary': teachers_salary,
        'students_fees': students_fees,
        'notices': notices,
    }

    return render(request, 'admin_homepage.html', context)



@user_passes_test(is_admin)
def admin_notice_view(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.by = request.user.first_name
            notice.save()
            return redirect('notice')
    else:
        form = NoticeForm()
    context = {
        'form': form
    }
    return render(request, 'admin_notice.html', context)


@user_passes_test(is_admin)
def delete_notice_view(request, pk):
    notice = Notice.objects.get(id=pk).delete()
    return redirect('admin_homepage')

# ||||||||||||||||||||||| ALL ABOUT THE TEACHERS |||||||||||||||||||||||||||||||

@user_passes_test(is_admin)
def admin_teacher_homepage_view(request):
    return render(request, 'teachers/admin_teacher_homepage.html')


@user_passes_test(is_admin)
def admin_view_all_teachers_view(request):
    teachers = TeacherInfo.objects.filter(status=True)
    return render(request, 'teachers/admin_view_all_teachers.html', {'teachers': teachers})


@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    if request.method == 'POST':
        user_form = TeacherUserInfoForm(request.POST)
        teacher_form = TeacherInfoForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            group, created = Group.objects.get_or_create(name='TEACHER')
            user.groups.add(group)

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.status = True
            teacher.save()
            messages.success(request, 'New teacher added successfully.')
            return redirect('admin_teacher_homepage')
        else:
            errors = user_form.errors.get_json_data(escape_html=False)
            errors.update(teacher_form.errors.get_json_data(escape_html=False))

            error_list = ErrorList()
            for field,  field_errors in errors.items():
                for error in field_errors:
                    error_list.append(f"{field}: {error['message']}")

            messages.error(request, error_list)      
    else:
        user_form = TeacherUserInfoForm()
        teacher_form = TeacherInfoForm()

    context = {
        'user_form': user_form,
        'teacher_form': teacher_form,
    }

    return render(request, 'teachers/admin_add_teacher.html', context)


@user_passes_test(is_admin)
def admin_view_individual_teacher_info_view(request, pk):
    teacher = TeacherInfo.objects.get(id=pk)
    payments = Payment.objects.filter(user_id=teacher.user_id).order_by('-date')
    daily_fees_taken = payments.values('date').order_by(
        '-date').annotate(sum=Sum('amount'))
    all_payments_taken = payments.aggregate(Sum('amount'))['amount__sum']

    if request.method == 'POST':
        if 'delete_teacher' in request.POST:
            teacher.status = False
            teacher.save()
            messages.success(request, 'Deleting teacher was successful')
            return redirect ('admin_view_all_teachers')
        else:
            messages.error(request, 'Could not delete teacher. Please try again.')
            return redirect('admin_view_individual_teacher_info', pk)
    context = {
        'teacher' : teacher,
        'payments': payments,
        'daily_fees_taken': daily_fees_taken,
        'all_payments_taken': all_payments_taken
    }
    return render(request, 'teachers/admin_view_individual_teacher_info.html', context)


@user_passes_test(is_admin)
def admin_update_individual_teacher_info_view(request, pk):
    teacher = TeacherInfo.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)

    form1 = TeacherUserInfoForm(instance=user)
    form2 = TeacherInfoForm(instance=teacher)

    if request.method == 'POST' and 'update' in request.POST:
        form1 = TeacherUserInfoForm(request.POST, instance=user)
        form2 = TeacherInfoForm(request.POST, instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.save()
            messages.success(request, 'Updating Teacher was successful')
            return redirect('admin_view_all_teachers')
        else:
            messages.error(request, 'Could not update teacher')
            return redirect('admin_view_all_teachers')
    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'teachers/admin_update_individual_teacher_info_view.html', context)



@user_passes_test(is_admin)
def admin_approve_teachers_view(request):
    applied_teachers = TeacherInfo.objects.filter(status=False)

    context = {
        'applied_teachers': applied_teachers,
    }
    return render(request, 'teachers/admin_approve_teachers.html', context)

# ||||||||||||||||||||||| END ALL ABOUT THE TEACHERS |||||||||||||||||||||||||||||||


# ||||||||||||||||||||||| ALL ABOUT THE STUDENTS |||||||||||||||||||||||||||||||



@user_passes_test(is_admin)
def admin_student_homepage_view(request):
    return render(request, 'students/students_general/admin_student_homepage.html')



@user_passes_test(is_admin)
def admin_view_all_students_view(request):
    students = StudentInfo.objects.filter(status=True)
    context = {
        'students': students,
    }
    return render(request, 'students/students_general/admin_view_all_students.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    if request.method == 'POST':
        user_form = StudentUserInfoForm(request.POST)
        student_form = StudentInfoForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            my_student_group, created = Group.objects.get_or_create(name='STUDENT')
            my_student_group.user_set.add(user)

            student = student_form.save(commit=False)
            student.user = user
            student.status = True
            if student.payment_method == 'Pay_Per_Day':
                student.termly_debt = 0
            student.save()
            messages.success(request, 'Adding student was successful.')
            return redirect('admin_student_homepage')      
    else:    
        user_form = StudentUserInfoForm()
        student_form = StudentInfoForm() 


    errors = user_form.errors.get_json_data(escape_html=False)
    errors.update(student_form.errors.get_json_data(escape_html=False))

    error_list = ErrorList()
    for field, field_errors in errors.items():
        for error in field_errors:
            error_list.append(f"{field}: {error['message']}")

    messages.error(request, error_list)         
    context = {
        'user_form': user_form,
        'student_form': student_form,
    }
    return render(request, 'students/students_general/admin_add_student.html', context)



@user_passes_test(is_admin)
def admin_approve_students_view(request):
    students = StudentInfo.objects.filter(status=False)

    context = {
        'students': students,
    }
    return render(request, 'students/students_general/admin_approve_students.html', context)



@user_passes_test(is_admin)
def admin_approve_or_decline_student_view(request, pk):
    if request.method == 'POST':
        if 'approve' in request.POST:
            student = StudentInfo.objects.get(id=pk)
            student.status = True
            student.save()
            messages.success(request, 'Student is now approved')
        elif 'decline' in request.POST:
            student = StudentInfo.objects.get(id=pk)
            student.delete()
    return redirect('admin_approve_students')



@user_passes_test(is_admin)
def admin_view_individual_student_info_view(request, pk):
    student = StudentInfo.objects.get(id=pk)
    payment_records = student.payment_set.all().order_by('-id')
    daily_canteen_record = payment_records.aggregate(daily_canteen=Sum('canteen'))
    daily_bus_record = payment_records.aggregate(daily_bus=Sum('bus_fee'))
    daily_tuition_record = payment_records.aggregate(
        daily_tuition=Sum('school_fees'))
    if request.method == 'POST':
        if 'delete_student' in request.POST:
            student.status = False
            student.save()
            messages.success(request, 'Deleting student was successful')
            return redirect('admin_view_all_students')
        else:
            messages.error(request, 'Could not delete student. Please try again.')
            return redirect('admin_view_individual_student_info', pk)

    context = {
        'student': student,
        'payment_records': payment_records,
        'daily_canteen_record': daily_canteen_record,
        'daily_bus_record': daily_bus_record,
        'daily_tuition_record': daily_tuition_record,
    }
    return render(request, 'students/students_general/admin_view_individual_student_info.html', context)



@user_passes_test(is_admin)
def admin_update_individual_student_info_view(request, pk):
    student = StudentInfo.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    form1 = StudentUserInfoForm(instance=user)
    form2 = StudentInfoForm(instance=student)
    if request.method == 'POST':
        form1 = StudentUserInfoForm(request.POST, instance=user)
        form2 = StudentInfoForm(request.POST, instance=student)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            if f2.payment_method == 'School_Fees_Aside':
                f2.termly_debt = 210
            f2.save()
            messages.success(request, 'Updating Student was successful')
            return redirect('admin_view_individual_student_info', pk)
        else:
            messages.error(request, 'Could not update student')
            return redirect('admin_view_individual_student_info', pk)

    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'students/students_general/admin_update_individual_student_info.html', context)


# ||||||||||||||||||||||| ALL STUDENTS PAYMENT |||||||||||||||||||||||||||||||




@user_passes_test(is_admin)
def admin_students_to_pay_view(request):
    students = StudentInfo.objects.filter(status=True, checkifpaiddaily=False).exclude(form_of_transportation='Walk', payment_method='School_Fees_Aside')
    all_students = StudentInfo.objects.filter(
        status=True, checkifpaiddaily=True)
    students_paying_per_day = StudentInfo.objects.filter(status=True, payment_method='Pay_Per_Day')
    if request.method == 'POST':
        all_students.update(checkifpaiddaily=False)
        students_paying_per_day.update(termly_debt=0)

    context = {
        'students': students,
    }
    return render(request, 'students/daily_payments/admin_students_to_pay.html', context)



@user_passes_test(is_admin)
def admin_student_daily_payment_view(request, pk):
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
            return redirect('admin_students_to_pay')
    context = {
        'student': student,
        'payment_form': payment_form,
        'student_previous_payments': student_previous_payments,
        'daily_school_fees': daily_school_fees,
    }
    return render(request, 'students/daily_payments/admin_student_daily_payment_page.html', context)

def get_base_fee(request, pk):
    student = StudentInfo.objects.get(id=pk)
    base_fee = student.get_base_fee()
    return JsonResponse({'base_fee': base_fee})


@user_passes_test(is_admin)
def admin_view_records_of_payment_view(request):
    page_obj = Payment.objects.all().order_by('-id')
    limit_data = Paginator(page_obj, 50)
    page_number = request.GET.get('page')
    try:
        records = limit_data.get_page(page_number)
    except PageNotAnInteger:
        records = limit_data.page(1)
    except EmptyPage:
        records = limit_data(limit_data.num_pages)
    context = {
        'records': records,
    }

    return render(request, 'students/daily_payments/admin_view_records_of_payment.html', context)



@user_passes_test(is_admin)
def admin_view_history_of_daily_total_payment_view(request):

    daily_fee_money_record_obj = Payment.objects.filter().values('date').order_by(
        '-date').annotate(sum=Sum('amount'), sum2=Sum('bus_fee'), sum3=Sum('school_fees'))
        
    daily_school_fee_money_record = SchoolFeesPayment.objects.filter().values(
        'date').order_by('date').annotate(sum4=Sum('school_fees'))

    limit_data = Paginator(daily_fee_money_record_obj, 7)
    page_number = request.GET.get('page')
    try:
        daily_fee_money_record = limit_data.get_page(page_number)
    except PageNotAnInteger:
        daily_fee_money_record = limit_data.page(1)
    except EmptyPage:
        daily_fee_money_record = limit_data(limit_data.num_pages)

    context = {
        'daily_fee_money_record': daily_fee_money_record,
        'daily_school_fee_money_record': daily_school_fee_money_record,
    }
    return render(request, 'students/daily_payments/admin_view_history_of_daily_total_payment.html', context)



@user_passes_test(is_admin)
def admin_daily_paid_students_view(request):
    students = StudentInfo.objects.filter(status=True, checkifpaiddaily=True)
    student_last_payments = {}

    for student in students:
        last_payment = Payment.objects.filter(student=student).last()
        student_last_payments[student] = last_payment

    context = {
        'student_last_payments': student_last_payments
    }
    return render(request, 'students/daily_payments/admin_daily_paid_students.html', context)



@user_passes_test(is_admin)
def admin_delete_daily_paid_student_view(request, pk):
    students_paid = StudentInfo.objects.get(id=pk)
    last_payment = Payment.objects.filter(student=students_paid)
    delete_last = last_payment.last()
    if request.method == 'POST':
        delete_last.delete()
        students_paid.checkifpaiddaily = False
        students_paid.save()

    return redirect('admin_daily_paid_students')


"""
Deletes a payment record for a student.

Parameters:
- request (HttpRequest): The request object. 
- pk (int): The primary key of the payment record to delete.

Returns:
- HttpResponse: Redirects to the view for that student's profile on success, 
                or back to the view all students page on failure.
"""

@user_passes_test(is_admin)
def admin_delete_payment_from_student_profile_view(request, pk):
    if request.method == 'POST':
        payment = Payment.objects.get(id=pk)
        if 'delete_payment' in request.POST:
            payment.delete()
            payment.student.checkifpaiddaily = False
            payment.student.save()
            messages.success(request, 'Deleting payment was successful')
            return redirect('admin_view_individual_student_info', str(payment.student_id))
        else:
            messages.error(request, 'Could not delete this payment')
            return redirect('admin_view_individual_student_info', str(payment.student_id))
    return redirect('admin_view_all_students')



@user_passes_test(is_admin)
def admin_students_to_pay_termly_view(request):
    students = StudentInfo.objects.filter(
        status=True, checkifpaidterm=False)
    student = StudentInfo.objects.all()
    all_students = StudentInfo.objects.filter(
        status=True, checkifpaidterm=True)
    if request.method == 'POST':
        all_students.update(checkifpaidterm=False)

        next_class = {
            'F & B': 'P.S.',
            'P.S.': 'K.S.A.',
            'K.S.A.': 'K.S.B.',
            'K.S.B.': 'K.S.C.',
            'K.S.C.': 'L.S.A.',
            'L.S.A.': 'L.S.B.',
            'L.S.B.': 'L.S.C.'
        }

        students_to_update = []
        for cls in student:
            if cls.grade in next_class:
                cls.grade = next_class[cls.grade]
                students_to_update.append(cls)

        if students_to_update:
            StudentInfo.objects.bulk_update(students_to_update, ['grade']) 

        StudentInfo.objects.filter(payment_method='School_Fees_Aside').update(termly_debt=F('termly_debt')+210, troll=False, soap=False, broom=False)
        StudentInfo.objects.filter(payment_method='Pay_Per_Day').update(termly_debt=0, troll=False, soap=False, broom=False)

    context = {
        'students': students
    }

    return render(request, 'students/termly_payments/admin_students_to_pay_termly.html', context)



@user_passes_test(is_admin)
def admin_student_termly_payment_view(request, pk):
    student = StudentInfo.objects.get(id=pk)
    form = TermlyPaymentForm(initial={'student': student})
    student_previous_schoolfees_payments = student.schoolfeespayment_set.all()
    if request.method == 'POST':
        form = TermlyPaymentForm(request.POST)
        if form.is_valid():
            deb = form.cleaned_data['debt']
            student.termly_debt = deb
            student.troll = form.cleaned_data['troll']
            student.soap = form.cleaned_data['soap']
            student.broom = form.cleaned_data['broom']
            if form.cleaned_data['debt'] == 0 or form.cleaned_data['debt'] is None and form.cleaned_data['troll'] == True and form.cleaned_data['soap'] == True and form.cleaned_data['broom'] == True:
                student.checkifpaidterm = True
            student.save()
            form.save()
        return redirect('admin_students_to_pay_termly')
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'students/termly_payments/admin_student_termly_payment_page.html', context)



@user_passes_test(is_admin)
def admin_termly_paid_students_view(request):
    students = StudentInfo.objects.filter(checkifpaidterm=True)
    context = {'students': students}

    return render(request, 'students/termly_payments/admin_termly_paid_students.html', context)



@user_passes_test(is_admin)
def admin_delete_termly_paid_student_view(request, pk):
    students_paid = StudentInfo.objects.get(id=pk)
    last_payment = SchoolFeesPayment.objects.filter(student=students_paid)
    delete_last = last_payment.last()
    if request.method == 'POST':
        delete_last.delete()
        students_paid.checkifpaidterm = False
        students_paid.save()

    return redirect('admin_termly_paid_students')



@user_passes_test(is_admin)
def admin_records_of_all_schoolfees_payment_view(request):
    page_obj = SchoolFeesPayment.objects.all().order_by('-id')
    limit_data = Paginator(page_obj, 50)
    page_number = request.GET.get('page')
    try:
        records = limit_data.get_page(page_number)
    except PageNotAnInteger:
        records = limit_data.get_page(1)
    except EmptyPage:
        records = limit_data(limit_data.num_pages)
    context = {'records': records}
    return render(request, 'students/termly_payments/admin_records_of_all_schoolfees_payment.html', context)



@user_passes_test(is_admin)
def admin_students_with_debt_view(request):
    students = StudentInfo.objects.all()
    context = {
        'students': students
    }
    return render(request, 'students/students_general/admin_students_with_debt.html', context)


# ||||||||||||||||||||||| END OF ALL STUDENTS PAYMENT |||||||||||||||||||||||||||||||
