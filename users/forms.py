"""
# -> UserRegisterForm: Register new users with the help of Django's native UserChangeForm.
# -> UserConfirmForm: activate the user from the key sent to him by email.
# -> PasswordResetForm: get the email of the user who wants to change the password
# -> PasswordResetForm: change user password.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.mail.message import EmailMessage

from .models import User, UserConfirmModel


class UserRegisterForm(UserCreationForm):
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
            to=['contato@fusion.com.br'],
            headers={'Reply-To': email}
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
    key = forms.CharField(max_length=6, min_length=6,
                          widget=forms.TextInput(attrs={'oninput': 'upperCase(this)'}))

    # 'clean_[field]' functions are responsible for treating the POST form data before reaching the database.
    # In this case, it is checking if the 'key' passed by the user matches the 'key' generated by the system.
    # The logic is to get the value of the form and the corresponding one saved in the database, captured from the
    # pk value of the view form ConfirmUserView.
    def clean_key(self):
        # Get all values defined in the form into a python dictionary.
        cleaned_data = self.cleaned_data
        # Get the corresponding 'key' value from the form.
        key_form = cleaned_data['key']
        # Capture the pk of the form
        pk = self.instance.pk
        # Append the user's 'key' to the variable by 'pk'.
        key_model = UserConfirmModel.objects.get(user=pk).key

        # If the keys are not the same or have a length different from 6, display the error 'Key error'.
        if key_model != key_form or len(key_form) != 6:
            raise forms.ValidationError("Key error")

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
            to=['contato@fusion.com.br'],
            headers={'Reply-To': email}
        )
        mail.send()


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nova senha',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Qual a nova senha?'}))
    new_password2 = forms.CharField(label='Confirmação de senha',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Repetir a nova senha'}))