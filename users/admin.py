"""
-> UserAdmin: Custom admin template for the User template that extends the standard UserAdmin class provided by Django.
# -> ConfirmUser: register the UserConfirmModel model in the Django admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import UserCreationForm
from .models import User, UserConfirmModel


@admin.register(User)
class UserAdmin(UserAdmin):
    # Add a custom user creation form.
    add_form = UserCreationForm

    # Define the fields shown in the table.
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'pk')

    # The fieldsets variable is used to define the sets of fields displayed for a template in the dashboard
    # Django administration. Lets you group related fields into distinct sections and customize how
    # these fields are displayed and arranged on the template edit page.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


@admin.register(UserConfirmModel)
class ConfirmUser(admin.ModelAdmin):
    # Define the fields shown in the table.
    list_display = ('user', 'key')
