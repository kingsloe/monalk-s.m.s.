from django.contrib.auth.models import User, Group

def add_student_to_group(username_targeted_part, targeted_group_name):
    username = username_targeted_part
    students = User.objects.filter(username__startswith=username)
    group = Group.objects.get(name=targeted_group_name)

    for student in students:
        try:
            group.user_set.add(student)
        except Exception as e:
            print(f'There was an error: {e}')
            print(f'Successfully added {len(students)} students to the {targeted_group_name} group.')
            
def run():
    add_student_to_group('MEC', 'STUDENT')
    add_student_to_group('Mec', 'STUDENT')
    add_student_to_group('mec', 'STUDENT')