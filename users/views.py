"""
-> LoginView: based on FormView responsible for generating the user's Login page if he is not yet logged in or opening
the home page if he is logged in.
-> UserRegisterView: based on CreateView responsible for generating a user registration page.
-> ConfirmUserView: based on UpdateView responsible for generating the registration confirmation page.
-> PasswordResetView: based on TemplateView responsible for generating the link submission page password recovery.
-> CustomPasswordResetConfirmView: based on PasswordResetConfirmView responsible for generating the password reset
page password.
"""
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import urlsafe_base64_encode

from django.views.generic import CreateView, FormView, UpdateView

from LivroBook import settings
from .models import User, UserConfirmModel
from .forms import UserRegisterForm, UserConfirmForm, PasswordResetForm, CustomPasswordResetConfirmForm

import string
import random


# Function to create the user confirmation key randomly with numbers and letters with size 6.
def random_key_value():
    # Defines a string containing all uppercase letters and digits.
    chars = string.ascii_uppercase + string.digits

    # Defines the number of characters that will have the random value.
    size = 6

    # Combines all generated characters into a single string, forming the 6-character random key.
    return ''.join(random.choice(chars) for _ in range(size))


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('book:index')

    # It is used to determine which templates should be used to render the view.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('book:index')
        return super().get(request, *args, **kwargs)

    # The form_valid() method is a standard Django method for when the submitted form is valid.
    def form_valid(self, form):
        # Retrieve form input "email".
        username = form.cleaned_data['username']
        # Retrieve "password" from form input
        password = form.cleaned_data['password']
        # Store the recovered data.
        user = authenticate(self.request, username=username, password=password)

        # If user differs from None, that is, the credentials are valid, the user is authenticated by calling the
        # login() function, passing the request and the user object.
        # If the credentials are invalid, the form.add_error() function is used to add an error to the form.
        if user is not None:
            # Persist a user ID on the backend of the request.
            login(self.request, user)
        else:
            form.add_error(None, 'Credenciais inválidas')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Get the "username" filled in the form.
        username = form.cleaned_data['username']
        # Get the "password" filled in the form.
        password = form.cleaned_data['password']

        # Try - Except responsible for checking if the user exists in the database, if it exists, the problem is in the
        # wrong password, if it does not exist, the login problem is in the user's existence.
        try:
            # Locate the user by the username passed in the form.
            user = User.objects.get(username=username)

            # Only the password is incorrect.
            if not user.check_password(password):
                form.add_error('password', 'A senha está incorreta.')
                return self.render_to_response(self.get_context_data(form=form))

        # User isn't found in the User database.
        except User.DoesNotExist:
            form.add_error('username', 'Usuário não encontrado.')
            return self.render_to_response(self.get_context_data(form=form))

        return super().form_invalid(form)


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'

    # It is used to determine which templates should be used to render the view.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('book:index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Save data in the Create User model.
        create_user = form.save()

        # Create instance for the Confirm User model.
        confirm_user = UserConfirmModel()
        confirm_user.key = random_key_value()
        # Relate the model
        confirm_user.user = create_user

        # Save model 2
        confirm_user.save()

        form.send_mail()

        return super().form_valid(form)

    # The get_success_url() method is used to determine the redirect URL after successful form submission.
    # Will send to 'confirm' page based on current user pk.
    def get_success_url(self):
        return self.object.get_absolute_url()


class UserConfirmView(UpdateView):
    model = User
    form_class = UserConfirmForm
    template_name = 'confirm.html'
    success_url = reverse_lazy('book:index')

    def form_valid(self, form):
        key = form.cleaned_data['key']
        try:
            UserConfirmModel.objects.get(key=key)
        except UserConfirmModel.DoesNotExist:
            form.add_error('key', 'A chave não é igual à enviada por e-mail. Favor verificar novamente.')
            return super().form_invalid(form)

        response = super().form_valid(form)
        # Get the user object currently being edited using the method.
        user = self.get_object()
        # Set the user's is_active attribute to True.
        user.is_active = True
        # Save the user with the changes made.
        user.save()

        return response


class PasswordResetView(FormView):
    template_name = "password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form, *args, **kwargs):
        # Retrieve form input "email".
        email = form.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
            # Base64 encode the primary key and create the UUID64.
            uidb64 = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
            # Create the user token.
            token = default_token_generator.make_token(user)

            # Creation of the password recovery link.
            reset_url = f"{settings.BASE_URL}/password-reset/confirm/{uidb64}/{token}/"

            form.send_mail(reset_url)

            return super().form_valid(form)
        except User.DoesNotExist:
            form.add_error('email', 'Usuário não encontrado')

            return self.form_invalid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password-reset-confirm.html'
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('users:login')
