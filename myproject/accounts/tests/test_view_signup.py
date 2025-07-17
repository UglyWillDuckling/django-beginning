from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..views import signup


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")  # by name lookup -> url
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_view(self):
        view = resolve(
            "/signup/"
        )  # see to what the `signup` route resolves to, which view function
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(
            self.response, "csrfmiddlewaretoken"
        )  # simply test for the string

    def test_form_inputs(self):  # TODO: separate into a template test
        """
        View must contain 5 fields
        """
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessFullSignUpTests(TestCase):
    count = 0

    def setUp(self):
        self.home_url = reverse("home")
        data = {
            "username": "johnaa",
            "email": "john@example.com",
            "password1": "Abdef1245678",
            "password2": "Abdef1245678",
        }
        self.response = self.client.post(reverse("signup"), data)

        print(SuccessFullSignUpTests.count, self.response)
        SuccessFullSignUpTests.count += 1

    def test_redirect(self):
        """
        A valid form submission should redirect to home page
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_auth(self):
        """
        Create a new requestto an arbitrary page.
        The resulting response should now have a `user` in the context.
        """
        response = self.client.get(self.home_url)
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """
        An invalid form should return to the same page
        """
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
