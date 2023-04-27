"""
Django settings for PezeshkeKhodkarAPI project.

Generated by 'django-admin startproject' using Django 4.1.7.
"""

from pathlib import Path
from decouple import config
import sys

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent


# It reads secret key from .env in root folder
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django rest framework
    'admin_honeypot',  # Fake Admin Page
    'api',             # API app
    'pages',           # Web-pages
    'accounts',         # Accounts
    'captcha'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'PezeshkeKhodkarAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'pages/templates',
                 BASE_DIR / 'accounts/templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'PezeshkeKhodkarAPI.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Iran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images, ...)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEST = 'test' in sys.argv

# Django rest framework settings:
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
}
if TEST is False:
    REST_FRAMEWORK.update(
        {'DEFAULT_THROTTLE_RATES':
            {
                'uploads': '5/hour',
            }
        }
    )

# Configure renderer of (Django Rest Framework)
if DEBUG:
    REST_FRAMEWORK.update(
        {
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.BrowsableAPIRenderer',
            )
        }
    )
else:
    REST_FRAMEWORK.update(
        {
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
            )
        }
    )

MEDIA_ROOT = BASE_DIR / "userfiles"


# Configure SSL, HSTS, CSRF protection, XSS, Clickjacking protection and Allowed hosts
if DEBUG is False:
    ALLOWED_HOSTS = [config("ALLOWED_HOSTS")]

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    # HSTS
    SECURE_HSTS_SECONDS = 86400  # 1 day
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    CSRF_COOKIE_SECURE = True

    # XSS protection
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Clickjacking protection
    X_FRAME_OPTIONS = 'DENY'

# ReCaptcha
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_REQUIRED_SCORE = config("RECAPTCHA_REQUIRED_SCORE")

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
