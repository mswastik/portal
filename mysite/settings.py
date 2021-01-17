"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=!i%_#y66)=&ra6aw$&dlydkvxvy9r09#wxku15!jazwpi*hjx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','192.168.1.7','172.26.80.119']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dal',
    'dal_select2',
    'app1.apps.App1Config',
    'import_export',
    'widget_tweaks',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'crispy_forms',
    'crequest',
    'reversion',
    'tabular_permissions',
    'django.contrib.admin',
    #'django_select2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crequest.middleware.CrequestMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app1db',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

#USE_L10N = True

USE_TZ = True

SHORT_DATE_FORMAT = "d-m-Y"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/media/swastik/disk2/GoogleDrive/Dabur/mysite/app1/static/"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 102404
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG
X_FRAME_OPTIONS = 'SAMEORIGIN'
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"
RA_ADMIN_INDEX_PAGE = 'app1/index.html'

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
#SELECT2_CACHE_BACKEND = 'select2'

JAZZMIN_SETTINGS = {
    'show_ui_builder': True,
    'navigation_expanded': False,
    "changeform_format": "single",
    'topmenu_links': [
        # Url that gets reversed (Permissions can be added)
        {'name': 'Home',  'url': 'admin:index', 'permissions': ['auth.view_user']},

        # model admin to link to (Permissions checked against model)
        {'model': 'auth.User'},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {'app': 'app1'},
        {'name':'App1', 'url': 'index'}
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": True,
    "body_small_text": False,
    "navbar_small_text": False,
    "sidebar_nav_small_text": False,
    "accent": "accent-primary",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-primary",
    "brand_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "footer_small_text": False
}