from django.urls import path
from .views import (
    homepage_view,
    aboutus_view,
    send_email_view,
    login_view,
    signup_options_view,
)
from admin_app.views import admin_homepage_view
from students_app.views import student_homepage_view, non_approved_students_view
from teachers_app.views import teacher_homepage_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('aboutus/', aboutus_view, name='aboutus'),
    path('send-email/', send_email_view, name="send_email"),
    path('login/', login_view, name='login'),
    path('logout', LogoutView.as_view(
        template_name='general_homepage.html'), name='logout'),
    path('admin/admin-homepage/', admin_homepage_view, name='admin_homepage'),
    path('student/student-homepage/', student_homepage_view,
         name='student-homepage'),
    path('teacher/teacher-homepage/', teacher_homepage_view, name='teacher-homepage'),
    path('signup-options/', signup_options_view, name='signup_options'),
    path('non-approved/', non_approved_students_view, name='non-approved')
]
