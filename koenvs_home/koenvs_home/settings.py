"""
Django settings for koenvs_home project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os.path
from os import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#cgr07d&^4kf_s%sy69hde(@bm!f3w5bih2!n99nvu-eija-a3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'apps.params.apps.ParamsConfig',
    'apps.serial.apps.SerialConfig',
    'apps.dimming.apps.DimmingConfig',
    'apps.magnetics.apps.MagneticsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_matplotlib',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'koenvs_home.urls'

TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     'DIRS': [os.path.join(BASE_DIR, 'templates/jinja2')],
    #     'APP_DIRS': True,
    #     'OPTIONS': {'environment': 'jinja2.Environment',},
    # },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # /i if you want to work from root
        'DIRS': [os.path.join(BASE_DIR, 'templates/'), ],
        'APP_DIRS': True,  # /i enables searching in apps dirs
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'koenvs_home.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'main': {
        'NAME': 'db.sqlite3',
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'tests': {
        'NAME': 'tests.db',
        'ENGINE': 'django.db.backends.sqlite3'
    },
}
# /i gives you the option to put an environment variable called DJANGO_DATABASE
DATABASES['default'] = DATABASES[environ["DATABASE_USED"]
                                 ] if "DATABASE_USED" in environ.keys() else DATABASES['main']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


# /i static root is only useful for deployment! Every static file will be stored here
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
# /i static url
STATIC_URL = '/static/'
# /i run 'python manage.py collectstatic' to pull all static files stored in this directory to your STATIC ROOT
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )
# /i where to look for static files, commented out to look into separate apps

# Media Files
# /i where does root directory start
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# /i media url: where are media stored
MEDIA_URL = '/media/'

# /i improve shell
SHELL_PLUS = 'ipython'

IPYTHON_ARGUMENTS = [
    '--ext', 'autoreload',
]
