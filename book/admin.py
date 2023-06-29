'''
-> ConfirmUser: registers the UserConfirmModel model in the Django admin panel.
'''
from django.contrib import admin
from .models import BookRegisterModel


# A classe
@admin.register(BookRegisterModel)
class ConfirmUser(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'edition', 'npages', 'begin', 'finish', 'concluded', 'wish')
