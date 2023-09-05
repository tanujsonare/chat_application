from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.


class UserTestCase(TestCase):
    def test_user(self):
        name = 'Tanuj'
        password = 'hello'
        u = User(name=name)
        u.set_password(password)
        u.save()
        self.assertEqual(u.name, name)
        self.assertTrue(u.check_password(password))