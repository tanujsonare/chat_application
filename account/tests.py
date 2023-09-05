from django.test import TestCase
from account.models import User

# Create your tests here.


class UserTestCase(TestCase):
    def test_user(self):
        name = 'Test case user'
        password = 'hello'
        u = User(name=name)
        u.set_password(password)
        u.save()
        self.assertEqual(u.name, name)
        self.assertTrue(u.check_password(password))