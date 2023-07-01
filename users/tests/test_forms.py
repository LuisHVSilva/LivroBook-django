from django.test import TestCase
from django.core import mail

from users.forms import UserRegisterForm, UserConfirmForm, PasswordResetForm
from users.models import UserConfirmModel, User

data = {
    'email': 'test@example.com',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'password1': '?/ftU0lG=B!',
    'password2': '?/ftU0lG=B!'
}

key = '123456'


def errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(f"{field}: {error}")


class TestUserRegisterForm(TestCase):
    def test_send_mail(self):
        form = UserRegisterForm(data=data)
        if not form.is_valid():
            errors(form)

        self.assertTrue(form)

        user = form.save()
        self.assertIsNotNone(user)
        self.assertIsNotNone(UserConfirmModel(user=user, key=key))
        UserConfirmModel(user=user, key=key).save()

        form.send_mail()
        self.assertEqual(len(mail.outbox), 1)

        form_email = mail.outbox[0]
        self.assertEqual(form_email.subject, 'Confirmação de criação de usuário LivroBook')
        self.assertEqual(form_email.body, f'Olá, {user.first_name}, '
                                          f'\nFalta só mais um passo para fazer parte da nossa história.'
                                          f'\nO seu código de 6 dígitos é: \n{key}')
        self.assertEqual(form_email.from_email, 'livro@book.com.br')
        self.assertEqual(form_email.to, ['email-teste@example.com'])
        self.assertEqual(form_email.reply_to[0], user.email)


class TestUserConfirmForm(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='test@example.com', password='password')
        UserConfirmModel.objects.create(user=user, key='123456')

    def test_clean_key(self):
        user = User.objects.get(email='test@example.com')
        confirm_model = UserConfirmModel.objects.get(user=user)
        form = UserConfirmForm(data={'key': key}, instance=confirm_model)

        if not form.is_valid():
            errors(form)

        self.assertTrue(form.is_valid())


class TestPasswordResetForm(TestCase):
    def test_send_mail(self):
        form = PasswordResetForm(data=data)
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
        self.assertEqual(form_email.reply_to[0], data['email'])
