from django.contrib.auth.models import User, Group
from django.test import Client, TestCase
from django.urls import reverse
from key import ISADMINPASSWORD, ISADMINUSERNAME, NONADMINPASSWORD, NONADMINUSERNAME, TESTPASSWORD

class AdminAddStudentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_group = Group.objects.create(name='ADMIN')
        self.admin_user = User.objects.create_user(username=ISADMINUSERNAME, password=ISADMINPASSWORD)
        self.admin_user.groups.add(self.admin_group)
        self.admin_user.save()
        self.non_admin_user = User.objects.create_user(username=NONADMINUSERNAME, password=NONADMINPASSWORD)
        self.non_admin_user.save()

    def test_redirect_anonymous_user(self):
        response = self.client.get(reverse('admin_add_student'))
        self.assertRedirects(response, '/login/?next=/admin/add-student/')
        
    def test_allow_non_admin_user(self):
        self.client.login(username=NONADMINUSERNAME, password=NONADMINPASSWORD)
        response = self.client.get(reverse('admin_add_student'))
        self.assertEqual(response.status_code, 302)

    def test_allow_admin_user(self):
        self.client.login(username=ISADMINUSERNAME, password=ISADMINPASSWORD)
        response = self.client.get(reverse('admin_add_student'))
        self.assertEqual(response.status_code, 200)    
    
    def test_add_student_form_submission(self):
        self.client.login(username=ISADMINUSERNAME, password=ISADMINPASSWORD)
        data = {
            'first_name':'testuser', 
            'last_name':'testuser_last',
            'username':'MEC001', 
            'password':TESTPASSWORD,
            'roll':'MEC001', 
            'grade':'K.S.A.', 
            'mobile':'0242508379', 
            'fee':'20', 
            'status':'True',
            'date_of_admission':'2004-01-29', 
            'date_of_birth':'2004-01-29', 
            'gender':'Male', 
            'mother':'mother', 
            'father':'father',
            'town': 1, 
            'foodfee':'0', 
            'payment_category':'Pay_Everything', 
            'payment_method':'Pay_Per_Day',
            'form_of_transportation':'Bus', 
            'passport':'passport',
        }
        response = self.client.post(reverse('admin_add_student'), data)
        self.assertEqual(response.status_code, 302)