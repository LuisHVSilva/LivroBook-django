from datetime import date, timedelta

from django.test import TestCase, RequestFactory
from django.urls import reverse

import users.tests.constants as constants
from book.models import BookRegisterModel
from book.views import IndexView, BookRegisterView, BookAllView, BookUpdateView
from users.models import User

edition = "edition"
npages = 100
begin = date(2023, 1, 1)
finish = date.today()
concluded = False
wish = False


class TestIndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.index_url = reverse(constants.URL_BOOK_INDEX)

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.user.is_active = True
        self.book1 = BookRegisterModel.objects.create(user=self.user,
                                                      edition=edition,
                                                      npages=npages,
                                                      begin=begin,
                                                      finish=finish,
                                                      concluded=True,
                                                      wish=False)

        self.book2 = BookRegisterModel.objects.create(user=self.user,
                                                      edition=edition,
                                                      npages=npages,
                                                      begin=begin,
                                                      finish=None,
                                                      concluded=False,
                                                      wish=True)

    def test_get_context_data_and_graphic(self):
        self.assertTrue(self.user.is_authenticated)

        view = IndexView.as_view()

        # Cria uma instância de HttpRequest para simular a requisição GET
        request = self.factory.get(reverse(constants.URL_BOOK_INDEX))

        # Define o usuário autenticado na requisição
        request.user = self.user

        # Chama o método dispatch para processar a requisição
        response = view(request)

        # Verifica se a resposta tem statos 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica o contexto retornado pelo método get_context_data
        context = response.context_data
        self.assertIn('added', context)
        self.assertIn('wish', context)
        self.assertIn('wish_table', context)
        self.assertIn('wish_graphic', context)
        self.assertIn('nbook', context)
        self.assertIn('npages', context)
        self.assertIn('book', context)
        self.assertIn('pages', context)

        # Verificar se o conteúdo de cada um está certo
        self.assertEquals(context['added'][0]['id'], 2)
        self.assertEquals(context['added'][0]['user_id'], 1)
        self.assertEquals(context['added'][0]['edition'], 'edition')
        self.assertEquals(context['added'][0]['npages'], 100)
        self.assertEquals(context['added'][0]['begin'], date(2023, 1, 1))
        self.assertEquals(context['added'][0]['finish'], '-')
        self.assertEquals(context['added'][0]['concluded'], 'Desejo')
        self.assertEquals(context['added'][0]['wish'], True)
        self.assertEquals(context['added'].count(), 2)

        self.assertIsNotNone(context['wish'])
        self.assertIsNotNone(context['wish_table'])
        self.assertEquals(context['wish_graphic'], 1)
        self.assertEquals(context['nbook'], [{1: 0}, {2: 0}, {3: 0}, {4: 0}, {5: 0}, {6: 0},
                                             {7: 1}, {8: 0}, {9: 0}, {10: 0}, {11: 0}, {12: 0}])
        self.assertEquals(context['npages'], [{1: 0}, {2: 0}, {3: 0}, {4: 0}, {5: 0}, {6: 0},
                                              {7: 100}, {8: 0}, {9: 0}, {10: 0}, {11: 0}, {12: 0}])
        self.assertEquals(context['book'], 1)
        self.assertEquals(context['pages'], 100)


class TestBookRegisterView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.book_register_url = reverse(constants.URL_BOOK_REGISTER)

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.user.is_active = True

    def test_form_valid(self):
        self.assertTrue(self.user.is_authenticated)
        form_data = {
            'user': self.user,
            'title': 'title1',
            'edition': edition,
            'npages': npages,
            'begin': begin,
            'finish': finish,
            'concluded': True,
            'wish': False
        }

        request = self.factory.post(self.book_register_url, data=form_data)
        request.user = self.user

        view = BookRegisterView.as_view()
        response = view(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse(constants.URL_BOOK_INDEX))

    def test_form_valid_type_error(self):
        self.assertTrue(self.user.is_authenticated)
        form_data = {
            'user': self.user,
            'title': 'title1',
            'edition': edition,
            'npages': npages,
            'concluded': True,
            'wish': False
        }

        request = self.factory.post(self.book_register_url, data=form_data)
        request.user = self.user

        view = BookRegisterView.as_view()
        response = view(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse(constants.URL_BOOK_INDEX))

    def test_form_invalid_begin_date(self):
        self.assertTrue(self.user.is_authenticated)
        form_data = {
            'user': self.user,
            'title': 'title1',
            'edition': edition,
            'npages': npages,
            'begin': date(2023, 2, 2),
            'finish': date(2023, 2, 1),
            'concluded': True,
            'wish': False
        }

        request = self.factory.post(self.book_register_url, data=form_data)
        request.user = self.user

        view = BookRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('finish' in form.errors)
        error_message = form.errors['finish'][0]
        self.assertEqual(error_message, 'Data de início deve ser menor que data final')

    def test_form_invalid_finish_date(self):
        self.assertTrue(self.user.is_authenticated)
        form_data = {
            'user': self.user,
            'title': 'title1',
            'edition': edition,
            'npages': npages,
            'begin': begin,
            'finish': date.today() + timedelta(days=1),
            'concluded': True,
            'wish': False
        }

        request = self.factory.post(self.book_register_url, data=form_data)
        request.user = self.user

        view = BookRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('finish' in form.errors)
        error_message = form.errors['finish'][0]
        self.assertEqual(error_message, 'Data de término deve ser menor que a data de hoje')


class TestBookAllView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.index_url = reverse(constants.URL_BOOK_INDEX)

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.user.is_active = True
        self.book = BookRegisterModel.objects.create(user=self.user,
                                                     title='title',
                                                     edition=edition,
                                                     npages=npages,
                                                     begin=begin,
                                                     finish=finish,
                                                     concluded=True,
                                                     wish=False)
        self.book2 = BookRegisterModel.objects.create(user=self.user,
                                                      concluded=False,
                                                      wish=True)

    def test_get_context_data(self):
        self.assertTrue(self.user.is_authenticated)
        view = BookAllView.as_view()

        # Cria uma instância de HttpRequest para simular a requisição GET
        request = self.factory.get(reverse(constants.URL_BOOK_ALL))

        # Define o usuário autenticado na requisição
        request.user = self.user

        # Chama o método dispatch para processar a requisição
        response = view(request)

        # Verifica se a resposta tem statos 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica o contexto retornado pelo método get_context_data
        context = response.context_data
        self.assertIn('data', context)
        self.assertEquals(context['data'][0]['id'], 1)
        self.assertEquals(context['data'][0]['user_id'], 1)
        self.assertEquals(context['data'][0]['title'], 'title')
        self.assertEquals(context['data'][0]['edition'], 'edition')
        self.assertEquals(context['data'][0]['npages'], 100)
        self.assertEquals(context['data'][0]['begin'], date(2023, 1, 1))
        self.assertEquals(context['data'][0]['finish'], date(2023, 7, 4))
        self.assertEquals(context['data'][0]['concluded'], 'Sim')
        self.assertEquals(context['data'][0]['wish'], 'Não')

        self.assertEquals(context['data'][1]['finish'], '-')
        self.assertEquals(context['data'][1]['concluded'], 'Não')
        self.assertEquals(context['data'][1]['wish'], 'Sim')

        self.assertEquals(context['data'].count(), 2)


class TestBookUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.index_url = reverse(constants.URL_BOOK_INDEX)

        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)
        self.user.is_active = True
        self.assertTrue(self.user.is_authenticated)

        self.book = BookRegisterModel.objects.create(user=self.user,
                                                     title='title',
                                                     edition=edition,
                                                     npages=npages,
                                                     begin=begin,
                                                     finish=finish,
                                                     concluded=True,
                                                     wish=False)

    def test_get_context_data(self):
        self.assertTrue(self.user.is_authenticated)

        # Cria uma instância de HttpRequest para simular a requisição GET
        request = self.factory.get(reverse(constants.URL_BOOK_ALL))

        # Define o usuário autenticado na requisição
        request.user = self.user

        view = BookUpdateView.as_view()

        # Chama o método dispatch para processar a requisição
        response = view(request, pk=self.book.pk)
        self.assertEqual(response.status_code, 200)

        # Verifica o contexto retornado pelo método get_context_data
        context = response.context_data
        self.assertIn('title', context)
        self.assertEquals(context['title'], 'title')

    def test_post_form_valid(self):
        form_data = {
            'title': 'New title'
        }

        request = self.factory.post(constants.URL_BOOK_UPDATE, data=form_data)
        request.user = self.user

        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.pk)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse(constants.URL_BOOK_INDEX))

    def test_form_invalid_begin_date(self):
        form_data = {
            'title': 'New title',
            'begin': date(2023, 2, 2),
            'finish': date(2023, 2, 1),
        }

        request = self.factory.post(constants.URL_BOOK_UPDATE, data=form_data)
        request.user = self.user

        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('finish' in form.errors)
        error_message = form.errors['finish'][0]
        self.assertEqual(error_message, 'Data de início deve ser menor que data final')

    def test_form_invalid_finish_date(self):
        form_data = {
            'title': 'New title',
            'begin': begin,
            'finish': date.today() + timedelta(days=1),
        }

        request = self.factory.post(constants.URL_BOOK_UPDATE, data=form_data)
        request.user = self.user

        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.pk)
        self.assertEqual(response.status_code, 200)

        # Verify that the form contains an error message
        form = response.context_data['form']
        self.assertTrue('finish' in form.errors)
        error_message = form.errors['finish'][0]
        self.assertEqual(error_message, 'Data de término deve ser menor que a data de hoje')

    def test_delete(self):
        request = self.factory.post(constants.URL_BOOK_UPDATE, data={'delete': True})
        request.user = self.user

        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.pk)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse(constants.URL_BOOK_INDEX))
