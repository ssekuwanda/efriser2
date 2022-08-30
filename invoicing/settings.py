from pathlib import Path
from django.contrib.messages import constants as messages
import os
from decouple import config
import dj_database_url

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ONLINE = False

ALLOWED_HOSTS = ['*']
CRISPY_TEMPLATE_PACK = 'bootstrap4'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'widget_tweaks',
    'mathfilters',
    'invoice',

    'qr_code',
    'django_bootstrap_icons',
    'markdownify',
    'accounts',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'invoicing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'invoice.context_processors.recaptcha',
            ],
            'libraries': {
            'custom_tags':'invoice.template_tags.custom_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'invoicing.wsgi.application'

# Postgres setup in production environment
if ONLINE:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
# STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

CSS_LOCATION = os.path.join(BASE_DIR,'static')

#Dynamic files and documents
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP Configure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

GOOGLE_RECAPTCHA_ENABLED = config("GOOGLE_RECAPTCHA_ENABLED", default=False)
GOOGLE_RECAPTCHA_SITE_KEY = config("GOOGLE_RECAPTCHA_SITE_KEY", default="")
GOOGLE_RECAPTCHA_SECRET_KEY = config("GOOGLE_RECAPTCHA_SECRET_KEY", default="")

MARKDOWNIFY = {
    "default": {
        "MARKDOWN_EXTENSIONS": [
            'markdown.extensions.fenced_code',
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ],
        "STRIP": False,
        "WHITELIST_TAGS": [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'strong',
            'ul',
            'code',
            'span',
            'div', 'class',
            'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        ],
        "WHITELIST_ATTRS": [
            'href',
            'src',
            'alt',
            'class',
        ],
        "WHITELIST_PROTOCOLS": [
            'http',
            'https',
        ]
    }
}