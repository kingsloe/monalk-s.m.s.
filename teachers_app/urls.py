from django.urls import path
from .views import teacher_signup_view

urlpatterns = [
    path('signup/', teacher_signup_view, name='teacher_signup')
]
