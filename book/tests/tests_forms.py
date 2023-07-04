from django.test import TestCase

from book.forms import BookRegisterForm

from datetime import date


class TestBookRegisterForm(TestCase):

    def test_form(self):
        data = {
            'title': "title",
            'edition': "edition",
            'npages': 100,
            'begin': date(2023, 1, 1),
            'finish': date.today(),
            'concluded': True,
            'wish': False,
        }

        form = BookRegisterForm(data=data)
        self.assertTrue(form)

    def test_clean_concluded_false(self):
        data = {
            'title': "title",
            'concluded': False,
        }

        form = BookRegisterForm(data=data)
        form.cleaned_data = data
        self.assertTrue(form.clean_concluded())

    def test_clean_concluded_true(self):
        data = {
            'title': "title",
            'concluded': True,
        }

        form = BookRegisterForm(data=data)
        form.cleaned_data = data
        self.assertFalse(form.clean_concluded())

    def test_clean_wish_false(self):
        data = {
            'title': "title",
            'wish': True,
        }
        form = BookRegisterForm(data=data)
        self.assertTrue(form)

        form.cleaned_data = data
        self.assertTrue(form.clean_wish())
        self.assertFalse(form.cleaned_data['concluded'])
