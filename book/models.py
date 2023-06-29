"""
-> BookRegisterModel: Database designated for the books that the user will register.
"""
from django.db import models
from users.models import User


class BookRegisterModel(models.Model):
    # "Models.OneToOneField" → User relationship: The UserConfirmModel model has a one-to-one relationship with user
    # model User using field user. This means that each User instance can have only one corresponding instance in
    # UserConfirmModel.
    # 'blank=True, null=True' → defines that the field accepts null values.
    # "title" → Book title.
    # "edition" → Book edition, can be null.
    # "npages" → number of book pages, can be null.
    # "begin" → initial day of reading, can be null.
    # "finish" → finishing day of reading, can be null.
    # "concluded" → if the book is finished, can be null.
    # "wish" → if the book is for wish list, can be null.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Título", max_length=100)
    edition = models.CharField("Edição", max_length=50, blank=True, null=True)
    npages = models.IntegerField("Número de páginas", blank=True, null=True)
    begin = models.DateField("Início", blank=True, null=True)
    finish = models.DateField("Fim", blank=True, null=True)
    concluded = models.BooleanField("Terminado?", default=False, blank=True, null=True)
    wish = models.BooleanField("Desejo", default=False, blank=True, null=True)

    class Meta:
        # Customize how the model's singular name is displayed in the Django admin.
        verbose_name = "Book"
        # Customize how the model's plural name is displayed in the Django admin.
        verbose_name_plural = "Books"
