import os
from pathlib import Path
from sensitve_data import SETTINGS_KEY
from sensitve_data import FACEBOOK_KEY, FACEBOOK_SECRET, INSTAGRAM_KEY, INSTAGRAM_SECRET, GOOGLE_KEY, GOOGLE_SECRET

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Change this password for your SECRET_KEY.
SECRET_KEY = SETTINGS_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',  # Social network authentication.
    'users',
    'book'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',  # Social network authentication.
]

ROOT_URLCONF = 'LivroBook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # Social network authentication.
                'social_django.context_processors.login_redirect',  # Social network authentication.
            ],
        },
    },
]

WSGI_APPLICATION = 'LivroBook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User Model Registration
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django's authentication.
    'social_core.backends.facebook.FacebookOAuth2',  # Facebook's authentication.
    'social_core.backends.google.GoogleOAuth2',  # Google's authentication.
    'social_core.backends.instagram.InstagramOAuth2',  # Instagram's authentication.
]

# Configurações para rede social.
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'
PROFILE_EXTRA_PARAMETERS = {'fields': 'id, name, email'}
EXTRA_DATA = [('name', 'name'), ('email', 'email')]
LOGIN_URL = 'users:login'
# Facebook's authentication settings.
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = PROFILE_EXTRA_PARAMETERS
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = EXTRA_DATA
# Google's authentication settings.
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_SECRET
SOCIAL_AUTH_GOOGLE_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_GOOGLE_PROFILE_EXTRA_PARAMS = PROFILE_EXTRA_PARAMETERS
SOCIAL_AUTH_GOOGLE_EXTRA_DATA = EXTRA_DATA
# Instagram's authentication settings.
SOCIAL_AUTH_INSTAGRAM_KEY = INSTAGRAM_KEY
SOCIAL_AUTH_INSTAGRAM_SECRET = INSTAGRAM_SECRET
SOCIAL_AUTH_INSTAGRAM_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = EXTRA_DATA
SOCIAL_AUTH_INSTAGRAM_PROFILE_EXTRA_PARAMS = PROFILE_EXTRA_PARAMETERS

# Use the environment variable if it's set, otherwise use the default development URL.
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')

# Send Email
# Testing ambient Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Production Email
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = 'no-reply@seudominio.com.br'
# EMAIL_PORT = 587
# EMAIL_USER_TLS = True
# EMAIL_HOST_PASSWORD = "senha"
