from django.urls import path
from .views import student_signup_view


urlpatterns = [
    path('signup/', student_signup_view, name='student_signup'),
]
