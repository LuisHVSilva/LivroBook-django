from django.test import TestCase
from book.models import BookRegisterModel

import users.tests.constants as constants
from users.models import User
from datetime import date

title = "title"
edition = "edition"
npages = 100
begin = date(2023, 1, 1)
finish = date.today()
concluded = False
wish = False


class TestBookRegisterModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email=constants.EMAIL, password=constants.PASSWORD)

    def test_crate_model(self):
        book = BookRegisterModel.objects.create(user=self.user,
                                                edition=edition,
                                                npages=npages,
                                                begin=begin,
                                                finish=finish,
                                                concluded=concluded,
                                                wish=wish)

        self.assertIsNotNone(book)
        self.assertEquals(book.user, self.user)
        self.assertEquals(book.edition, edition)
        self.assertEquals(book.npages, npages)
        self.assertEquals(book.begin, begin)
        self.assertEquals(book.finish, finish)
        self.assertEquals(book.concluded, concluded)
        self.assertEquals(book.wish, wish)
