"""
# -> UserManager: handle creating and managing users.
# -> User: defines a custom user template with additional fields, authentication settings, and methods
# custom.
# -> UserConfirmModel: confirmation key for a user
"""
from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


# The BaseUserManager is used to customize user creation logic, such as using a field email instead of a username field
# for authentication, add custom fields to user template, define additional restrictions during user creation, among
# other customizations.
class UserManager(BaseUserManager):
    # The _create_user function is an internal BaseUserManager method used to create a user.
    def _create_user(self, email, password, **extra_fields):
        # Check if the email was provided.
        if not email:
            raise ValueError("O email é obrigatório")

        # Match the email typed by the user to the right email pattern.
        email = self.normalize_email(email)
        # Defining email as the login method for the user.
        user = self.model(email=email, username=email, **extra_fields)
        # Set and encrypt the password.
        user.set_password(password)
        # Save the customer user model.
        user.save(using=self._db)

        return user

    # The function create_user is a public method of BaseUserManager that uses the internal method _create_user
    # to create a user with some default values.
    def create_user(self, email, password=None, **extra_fields):
        # Defines that the user is not a staff member.
        extra_fields.setdefault('is_staff', False)
        # Defines that the user is not a superuser member.
        extra_fields.setdefault('is_superuser', False)
        # Defines that the user is not an active member at the time of account creation.
        extra_fields.setdefault('is_active', False)

        return self._create_user(email, password, **extra_fields)

    # The function create_superuser is a public method of BaseUserManager that uses the internal method _create_user
    # to create a superuser with some default values.
    def create_superuser(self, email, password, **extra_fields):
        # Defines that the user is a staff member.
        extra_fields.setdefault('is_staff', True)
        # Defines that the user is a superuser member.
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super usuário não cadastrado")

        return self._create_user(email, password, **extra_fields)

    class Meta:
        use_in_migrations = True


class User(AbstractUser):
    # User-supplied information for additional fields
    # "email" → user email.
    # "first_name" → user-first name.
    # "last_name" → user-last name.
    email = models.EmailField('E-mail', max_length=200, unique=True)
    first_name = models.CharField("Primeiro nome", max_length=20)
    last_name = models.CharField("Sobrenome", max_length=50)

    # Automatic information saved in the bank.
    # "date_joined" → date and time of user registration set to 'now' by Django.
    date_joined = models.DateTimeField('Data de cadastro', auto_now_add=True)

    # User Model information.
    # USERNAME_FIELD → 'email' field is used as the unique identification field for authentication.
    # REQUIRED_FIELD → which additional fields are required when creating a user.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # This function returns the absolute URL for a specific user, based on their pk (primary key).
    def get_absolute_url(self):
        return f'/confirm/{self.pk}'

    # This function returns a string representation of the User object and the user's email.
    def __str__(self):
        return self.email

    # Responsible for managing user creation, including methods like create_user and create_superuser.
    objects = UserManager()


class UserConfirmModel(models.Model):
    # "Models.OneToOneField" → User Relationship: The UserConfirmModel model has a one-to-one relationship with user
    # model User using field user. This means that each User instance can have only one corresponding instance in
    # UserConfirmModel.

    # User-supplied information for additional fields
    # "user" → user email.
    # "key" → User confirmation key.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    key = models.CharField("key", max_length=6)

    # Automatic information saved in the bank.
    # "created" → automatically sets the date and time the field was created.
    created = models.DateTimeField('Data de cadastro', auto_now_add=True)

    class Meta:
        verbose_name = "Confirm User Key"
        verbose_name_plural = verbose_name
