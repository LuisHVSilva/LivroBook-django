""" -> CONSTANT DATA <- """
EMAIL = 'test@example.com'
PASSWORD = '?/ftU0lG=B!'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
KEY = '123456'

USER_DATA = {
    'email': EMAIL,
    'first_name': FIRST_NAME,
    'last_name': LAST_NAME,
    'password1': PASSWORD,
    'password2': PASSWORD
}


""" -> URLS AND TEMPLATES <- """
# USERS APP
URL_USERS_LOGIN = 'users:login'
TEMPLATE_USERS_LOGIN = 'login.html'
URL_USERS_REGISTER = 'users:register'
TEMPLATE_USERS_REGISTER = 'register.html'
URL_USERS_CONFIRM = 'users:confirm'
TEMPLATE_USERS_CONFIRM = 'confirm.html'
URL_USERS_PASSWORD_RESET = 'users:password_reset'

# BOOK APP
URL_BOOK_INDEX = 'book:index'
URL_BOOK_REGISTER = 'book:book-register'
TEMPLATE_BOOK_REGISTER = 'book-register.html'
URL_BOOK_ALL = 'book:book-all'
URL_BOOK_UPDATE = 'book:book-update'
