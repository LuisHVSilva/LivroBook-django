from django.shortcuts import redirect, resolve_url
from django.test import TestCase, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User, AnonymousUser

from users.models import User, UserConfirmModel

from users.views import random_key_value, LoginView, UserRegisterView, UserConfirmView, PasswordResetView

import users.tests.constants as constants


from django.contrib.auth import authenticate, login

class TestRandomKeyValue(TestCase):
    def test_result(self):
        random_key = random_key_value()
        self.assertEquals(len(random_key), 6)


class TestLoginView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.login_url = reverse(constants.URL_USERS_LOGIN)
        self.index_url = reverse(constants.URL_BOOK_INDEX)

        # Create a user for testing
        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.user.is_active = True

    def test_get_authenticated_user(self):
        request = self.factory.get(self.login_url)
        request.user = User.objects.get(email=self.user.email)

        view = LoginView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(constants.URL_BOOK_INDEX))

    def test_get_anonymous_user(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, constants.TEMPLATE_USERS_LOGIN)
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        # Set up the test client
        a = self.client.login(username=self.user.email, password=constants.PASSWORD)
        print('\n\n\n\n')
        print(a)

        form_data = {
            'username': constants.EMAIL,
            'password': constants.PASSWORD
        }


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.register_url = reverse(constants.URL_USERS_REGISTER)

    def test_get_authenticated_user(self):
        request = self.factory.get(self.register_url)
        request.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)

        view = UserRegisterView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(constants.URL_BOOK_INDEX))

    def test_get_anonymous_user(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, constants.TEMPLATE_USERS_REGISTER)
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        request = self.factory.post(self.register_url, data=constants.USER_DATA)
        request.user = AnonymousUser()

        view = UserRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=constants.EMAIL)
        self.assertTrue(User.objects.filter(username=constants.EMAIL).exists())
        self.assertTrue(UserConfirmModel.objects.filter(user=user).exists())

        redirected_url = response.url
        expected_url = reverse(constants.URL_USERS_CONFIRM, kwargs={'pk': user.pk})
        self.assertEqual(resolve_url(redirected_url), expected_url)

        follow_response = self.client.get(redirected_url)
        self.assertEqual(follow_response.status_code, 200)
        self.assertTemplateUsed(follow_response, constants.TEMPLATE_USERS_CONFIRM)


class TestUserConfirmView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.confirm_model = UserConfirmModel.objects.create(user=self.user, key=constants.KEY)

        self.url = reverse(constants.URL_USERS_CONFIRM, kwargs={'pk': self.user.pk})

    def test_valid_key(self):
        form_data = {
            'key': constants.KEY
        }

        request = self.factory.post(self.url, data=form_data)
        request.user = self.user

        view = UserConfirmView.as_view()
        response = view(request, pk=self.user.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(constants.URL_BOOK_INDEX))

        # Verifica se o usuário foi ativado
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_invalid_key(self):
        form_data = {
            'key': '654321'
        }

        request = self.factory.post(self.url, data=form_data)
        request.user = self.user

        view = UserConfirmView.as_view()
        response = view(request, pk=self.user.pk)

        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('key' in form.errors)
        error_message = form.errors['key'][0]
        self.assertEqual(error_message, 'A chave não é igual à enviada por e-mail. Favor verificar novamente.')

        # Refresh the user object from the database
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class TestPasswordResetView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.key = '123456'

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)

        self.url = reverse(constants.URL_USERS_PASSWORD_RESET)

    def test_form_valid(self):
        form_data = {
            'email': constants.EMAIL
        }

        request = self.factory.post(self.url, data=form_data)
        request.user = self.user

        view = PasswordResetView.as_view()
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(constants.URL_USERS_LOGIN))

    def test_nonexistent_user(self):
        form_data = {
            'email': 'email@nãoexiste.com'
        }

        request = self.factory.post(self.url, data=form_data)
        request.user = self.user

        view = PasswordResetView.as_view()
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('email' in form.errors)
        error_message = form.errors['email'][0]
        self.assertEqual(error_message, 'Usuário não encontrado')
