from django.test import TestCase

from users.models import User

from model_mommy import mommy


class TestUserManager(TestCase):
    def setUp(self):
        self.user = User.objects.create_user

    def test__create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            self.user(email=None, password='password')

        self.assertEqual(str(context.exception), 'O email é obrigatório')

    def test__create_user_without_password(self):
        with self.assertRaises(ValueError) as context:
            self.user(email='test@example.com', password=None)

        self.assertEqual(str(context.exception), 'Senha obrigatória')

    def test_normalize_email_except(self):
        with self.assertRaises(ValueError) as context:
            self.user(email='testexample.com', password='password')

        self.assertEqual(str(context.exception), 'O email não possui o padrão correto: email@dominio.com')

    def test_create_user(self):
        user = self.user('ABC@Teste.com', '1234')
        self.assertEquals(user.is_staff, False)
        self.assertEquals(user.is_superuser, False)
        self.assertEquals(user.is_active, False)
        self.assertEquals(user.email, 'abc@teste.com')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser("teste@example.com", 'password')
        self.assertEquals(superuser.is_staff, True)
        self.assertEquals(superuser.is_superuser, True)
        self.assertEquals(superuser.is_active, True)


class TestUser(TestCase):
    def setUp(self):
        self.user = mommy.make('users.User')

    def test_get_absolute_url(self):
        print('\n\n---Create_User test:')
        self.assertIsNotNone(self.user)
        self.assertEquals(self.user.get_absolute_url(), f'/confirm/{self.user.pk}')

    def test_str(self):
        print('\n\n---Create_User test:')
        self.assertIsNotNone(self.user)
        self.assertEquals(str(self.user), self.user.email)

    def teste_create_user(self):
        self.assertIsNotNone(self.user)
