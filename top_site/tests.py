'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com/

        /top_site/tests.py
            Django TestCases's
                UserCreationFormTestCase
'''
from django.test import TestCase
from django.contrib.auth.models import User

from .forms import UserCreationForm

# Create your tests here.
'''
UserCreationFormTestCase
    tests to exercise forms.UserCreationForm
        test_valid
        test_invalid
'''
class UserCreationFormTestCase(TestCase):
    def test_valid(self):
        form = UserCreationForm({
            "username": "user1",
            "first_name": "user",
            "password1": "1234pass",
            "password2": "1234pass"
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.first_name, "user")

    def test_invalid(self):
        form = UserCreationForm({
            "first_name": "user",
            "password1": "1234pass",
            "password2": "1234pass"
        })
        self.assertFalse(form.is_valid())

'''
TopSiteTestCase
    tests to ensure views and url routing is working
        test_index
        test_login
        test_register
        test_profile
'''
class TopSiteTestCase(TestCase):
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        #get register
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        #post register
        response = self.client.post("/register/", {"first_name": "user",
                                                   "username": "user1",
                                                   "password1": "1234pass",
                                                   "password2": "1234pass"})
        self.assertEqual(response.status_code, 302)

    def test_profile(self):
        #if not logged in redirect
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 302)
        user = User.objects.create_user("user", "user@intellproject.com", "blah")
        self.client.force_login(user)
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 200)
                        

