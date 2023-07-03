from django.test import TestCase

from users.models import User, UserConfirmModel
import users.tests.constants as constants


class TestUserManager(TestCase):

    # Test for creating user without email.
    def test__create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email=None, password=constants.PASSWORD)

        self.assertEqual(str(context.exception), 'O email é obrigatório')

    # Test for creating user without password.
    def test__create_user_without_password(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email=constants.EMAIL, password=None)

        self.assertEqual(str(context.exception), 'Senha obrigatória')

    # Test for email that is not in the correct format.
    def test_normalize_email_except(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email='testexample.com', password=constants.PASSWORD)

        self.assertEqual(str(context.exception), 'O email não possui o padrão correto: email@dominio.com')

    # Test to create user.
    def test_create_user(self):
        user = User.objects.create_user(constants.EMAIL, constants.PASSWORD)
        self.assertEquals(user.is_staff, False)
        self.assertEquals(user.is_superuser, False)
        self.assertEquals(user.is_active, False)
        self.assertEquals(user.email, constants.EMAIL)

    # Test to create user superuser.
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(constants.EMAIL, constants.PASSWORD)
        self.assertEquals(superuser.is_staff, True)
        self.assertEquals(superuser.is_superuser, True)
        self.assertEquals(superuser.is_active, True)


class TestUser(TestCase):
    def setUp(self):
        # Creating user
        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)

    # User creation test.
    def teste_create_user(self):
        self.assertIsNotNone(self.user)

    # Return URL test.
    def test_get_absolute_url(self):
        self.assertEquals(self.user.get_absolute_url(), f'/confirm/{self.user.pk}')

    # Model __str__ return test.
    def test_str(self):
        self.assertFalse(self.user.is_active)
        self.assertEquals(str(self.user), self.user.email)


class TestUserConfirmModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)

    # Test changing user from inactive to active.
    def test_create_model(self):
        confirm_model = UserConfirmModel.objects.create(user=self.user, key=constants.KEY)
        self.assertIsNotNone(confirm_model)
        self.assertEquals(confirm_model.user, self.user)
        self.assertEquals(confirm_model.key, "123456")
        self.assertIsNotNone(confirm_model.created)
