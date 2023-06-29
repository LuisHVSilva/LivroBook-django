"""
-> @method_decorator(login_required, name='dispatch'): if the user is not registered, it redirects the page to the login.
-> IndexView: website index page. Displays data and tables regarding the books already registered by the user.
-> BookRegisteView: page to register new books.
-> BookAllView: page to present a table with all the books already registered and their information.
-> BookUpdateView: page to update a previously registered book.
"""
from datetime import date

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, CreateView, UpdateView

from book.forms import BookRegisterForm
from users.decorators import login_required

from .models import BookRegisterModel


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Retrieve the logged-in user's email.
        pk = self.request.user.email

        # Create the data delivery variable.
        context = super().get_context_data(**kwargs)

        # Retrieves the first six values of the "BookRegisterModel" model based on the email.
        added = BookRegisterModel.objects.filter(user_id__email=pk).order_by('-id')[:6].values()

        for a in added:
            if a["concluded"] is False:
                a['concluded'] = "Não"
            else:
                a["concluded"] = "Sim"

            if a["wish"]:
                a['concluded'] = "Desejo"

            for key, value in a.items():
                if value is None or value == "":
                    a[key] = "-"

        # Create the 'added' list with the values retrieved from the database.
        context["added"] = added

        # Search all data that have 'wish' as true.
        context['wish'] = BookRegisterModel.objects.filter(user_id__email=pk, wish=True)
        # first six values of 'wish'.
        context['wish_table'] = context['wish'][:6].values()
        # Count how many 'wish' there are.
        context['wish_graphic'] = context['wish'].count()

        # Data related to books and pages read.
        context["nbook"], context["npages"], context["book"], context["pages"] = self.get_context_graphic()

        return context

    # Function to create the logic of division of books and pages read per month.
    # OBS: there Will only be books and pages that are completed.
    # OBS: the sum will be fully rolled back to the registration date of when the book was finished.
    def get_context_graphic(self):
        data = BookRegisterModel.objects.filter(user_id__email=self.request.user.email, concluded=True).values()
        dic_book = [{1: 0}, {2: 0}, {3: 0}, {4: 0}, {5: 0}, {6: 0},
                    {7: 0}, {8: 0}, {9: 0}, {10: 0}, {11: 0}, {12: 0}]
        dic_npages = [{1: 0}, {2: 0}, {3: 0}, {4: 0}, {5: 0}, {6: 0},
                      {7: 0}, {8: 0}, {9: 0}, {10: 0}, {11: 0}, {12: 0}]
        book = 0
        pages = 0

        for d in data:
            if d["finish"]:
                array = d["finish"].month - 1
                key = d["finish"].month
                book += 1
                dic_book[array][key] += 1
                if d["npages"]:
                    dic_npages[array][key] += d["npages"]
                    pages += d["npages"]

        return dic_book, dic_npages, book, pages


@method_decorator(login_required, name='dispatch')
class BookRegisterView(CreateView):
    model = BookRegisterModel
    form_class = BookRegisterForm
    template_name = "book-register.html"
    success_url = reverse_lazy('book:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        cleaned_data = form.cleaned_data

        # Check if the start date is greater than the end date, if true, return the error.
        try:
            if cleaned_data["begin"] > cleaned_data["finish"]:
                form.add_error('finish', 'Data de início deve ser menor que data final')
                return self.form_invalid(form)

            elif cleaned_data["finish"] > date.today():
                form.add_error('finish', 'Data de término deve ser menor que a data de hoje')
                return self.form_invalid(form)

        except TypeError:
            pass

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BookAllView(TemplateView):
    template_name = "book-all.html"

    def get_context_data(self, **kwargs):
        pk = self.request.user.email

        context = super().get_context_data(**kwargs)  # Cria a variável de entrega de dados.
        # Recupera os seis primeiros valores do modelo "BookRegisterModel" baseado no email.
        data = BookRegisterModel.objects.filter(user_id__email=pk).values()
        for d in data:
            if d["concluded"] is False:
                d['concluded'] = "Não"
            else:
                d["concluded"] = "Sim"

            if d["wish"]:
                d['wish'] = "Sim"
                d['concluded'] = "Não"
            else:
                d['wish'] = "Não"

            for key, value in d.items():
                if value is None or value == "":
                    d[key] = "-"

        context["data"] = data  # Cria a lista 'added' que com os valores recuperados do banco.

        return context


class BookUpdateView(UpdateView):
    model = BookRegisterModel
    template_name = 'book-update.html'
    form_class = BookRegisterForm

    def get_context_data(self, **kwargs):
        # Retrieve the logged-in user's email.
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context["title"] = BookRegisterModel.objects.get(pk=pk).title

        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            return self.delete(request, *args, **kwargs)
        else:
            return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.user = self.request.user
        cleaned_data = form.cleaned_data

        try:
            if cleaned_data["begin"] > cleaned_data["finish"]:
                form.add_error('finish', 'Data de início deve ser menor que data final')
                return self.form_invalid(form)

            elif cleaned_data["finish"] > date.today():
                form.add_error('finish', 'Data de término deve ser menor que a data de hoje')
                return self.form_invalid(form)

        except TypeError:
            pass

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book:index')
