from django.test import TestCase
from django.core import mail

from users.forms import UserRegisterForm, UserConfirmForm, PasswordResetForm
from users.models import UserConfirmModel, User

import users.tests.constants as constants


def errors(form):
    for field, message_errors in form.errors.items():
        for message in message_errors:
            print('\n---------------------')
            print(f"{field}: {message}")
            print('---------------------\n')


class TestUserRegisterForm(TestCase):
    def test_send_mail(self):
        form = UserRegisterForm(data=constants.USER_DATA)
        if not form.is_valid():
            errors(form)

        self.assertTrue(form)

        user = form.save()
        self.assertIsNotNone(user)
        self.assertIsNotNone(UserConfirmModel(user=user, key=constants.KEY))
        UserConfirmModel(user=user, key=constants.KEY).save()

        form.send_mail()
        self.assertEqual(len(mail.outbox), 1)

        form_email = mail.outbox[0]
        self.assertEqual(form_email.subject, 'Confirmação de criação de usuário LivroBook')
        self.assertEqual(form_email.body, f'Olá, {user.first_name}, '
                                          f'\nFalta só mais um passo para fazer parte da nossa história.'
                                          f'\nO seu código de 6 dígitos é: \n{constants.KEY}')
        self.assertEqual(form_email.from_email, 'livro@book.com.br')
        self.assertEqual(form_email.to, ['email-teste@example.com'])
        self.assertEqual(form_email.reply_to[0], user.email)


class TestUserConfirmForm(TestCase):
    def setUp(self):
        user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        UserConfirmModel.objects.create(user=user, key=constants.KEY)

    def test_clean_key(self):
        user = User.objects.get(email=constants.EMAIL)
        confirm_model = UserConfirmModel.objects.get(user=user)
        form = UserConfirmForm(data={'key': constants.KEY}, instance=confirm_model)

        if not form.is_valid():
            errors(form)

        self.assertTrue(form.is_valid())


class TestPasswordResetForm(TestCase):
    def test_send_mail(self):
        form = PasswordResetForm(data=constants.USER_DATA)
        if not form.is_valid():
            errors(form)

        self.assertTrue(form)
        link = "www.teste.com.br"
        form.send_mail(link)
        self.assertEqual(len(mail.outbox), 1)
        form_email = mail.outbox[0]
        self.assertEqual(form_email.subject, 'Recuperação de Senha')
        self.assertEqual(form_email.body, link)
        self.assertEqual(form_email.from_email, 'livro@book.com.br')
        self.assertEqual(form_email.to, ['email-teste@example.com'])
        self.assertEqual(form_email.reply_to[0], constants.USER_DATA['email'])
