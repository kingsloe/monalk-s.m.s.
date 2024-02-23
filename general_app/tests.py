from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from key import ISADMINPASSWORD, ISADMINUSERNAME, NONADMINPASSWORD, NONADMINUSERNAME

# Create your tests here.

class AdminLoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_group = Group.objects.create(name='ADMIN')
        self.admin_user = User.objects.create_user(username=ISADMINUSERNAME, password=ISADMINPASSWORD)
        self.admin_user.groups.add(self.admin_group)
        self.admin_user.save()

    def test_if_logged_in(self):
        self.client.login(username=ISADMINUSERNAME, password=ISADMINPASSWORD)
        response = self.client.get(reverse('admin-homepage'))
        self.assertEqual(response.status_code, 200)
