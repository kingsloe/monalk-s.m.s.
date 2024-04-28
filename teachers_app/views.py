from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from general_app.views import is_teacher
from .models import TeacherInfo

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
