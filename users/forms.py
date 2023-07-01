"""
# -> UserRegisterForm: Register new users with the help of Django's native UserChangeForm.
# -> UserConfirmForm: activate the user from the key sent to him by email.
# -> PasswordResetForm: get the email of the user who wants to change the password
# -> PasswordResetForm: change user password.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail.message import EmailMessage

from .models import User, UserConfirmModel


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="email", max_length=200,
                             widget=forms.EmailInput(attrs={'placeholder': 'Qual o seu email?'}))
    first_name = forms.CharField(label="Primeiro nome", max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'Qual o seu primeiro nome?'}))
    last_name = forms.CharField(label="Sobrenome", max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'E seu sobrenome?'}))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Qual a senha?'}))
    password2 = forms.CharField(label='Confirme de senha escrita acima',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repetir a nova senha'}))

    # Function "send_email" to configure the body of the email and send it to the user who just signed up.
    def send_mail(self):
        subject = "Confirmação de criação de usuário LivroBook"
        name = self.cleaned_data['first_name']
        email = self.cleaned_data['email']
        # Get the corresponding PK between the two models
        pk = User.objects.get(email=email).pk
        # Get key value inside ConfirmUser for confirmation
        key = UserConfirmModel.objects.get(user=pk).key

        body = f'Olá, {name}, ' \
               f'\nFalta só mais um passo para fazer parte da nossa história.' \
               f'\nO seu código de 6 dígitos é: ' \
               f'\n{key}'

        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email='livro@book.com.br',
            to=['email-teste@example.com'],
            reply_to=[email]
        )
        mail.send()

    # "Save" function used to fix some fields inside the User model before saving.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserConfirmForm(UserChangeForm):
    key = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'oninput': 'upperCase(this)'}))

    class Meta:
        model = User
        fields = ['key']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100)

    def send_mail(self, link):
        email = self.cleaned_data['email']
        subject = "Recuperação de Senha"
        body = link

        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email='livro@book.com.br',
            to=['email-teste@example.com'],
            reply_to=[email]
        )
        mail.send()


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nova senha',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Qual a nova senha?'}))
    new_password2 = forms.CharField(label='Confirmação de senha',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Repetir a nova senha'}))
