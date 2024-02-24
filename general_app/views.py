from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from students_app.models import StudentInfo
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='ADMIN')


def is_student(user):
    return user.groups.filter(name='STUDENT')


def is_teacher(user):
    return user.groups.filter(name='TEACHER')

def is_student_approved(user):
    return is_student(user) and StudentInfo.objects.filter(user_id=user.id, status=True).exists()

def get_user_homepage(user):
    if is_student_approved(user):
        return 'student-homepage'
    elif is_student_approved(user) == False:
        return 'non-approved'  
    elif is_admin(user):
        return 'admin-homepage'
    return 'homepage'            

def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_user_homepage(request.user))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(get_user_homepage(user))            
    return render(request, 'login.html')


def signup_options_view(request):
    return render(request, 'signup_options.html')


def homepage_view(request):
    return render(request, 'general_homepage.html')


def aboutus_view(request):
    return render(request, 'aboutus.html')


def send_email_view(request):
    if request.method == 'POST':
        template = render_to_string('email_template.txt', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['nanayawdjan446@gmail.com']
        )
        email.fail_silently = False
        email.send()
        messages.success(request, 'Reaching out to us was successfull.')
    return render(request, 'aboutus.html')
