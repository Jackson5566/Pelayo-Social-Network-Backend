"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&^_21q!(yq3_3ygyu)nkou^8@vyab-+!!0y^$6o_sl+=*m2tk0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#jackson782.pythonanywhere.com
ALLOWED_HOSTS = ['jackson782.pythonanywhere.com', 'https://pelayo-sn-media.b-cdn.net/']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users_app',
    'posts_app',
    'auth_app',
    'corsheaders',
    'contact_app',
    'rest_framework_simplejwt',
    'message_app',
    'django_filters',
    'news_app',
    'newspaper_app',
    'stdimage'
]

# https://jackson782.pythonanywhere.com/
CSRF_TRUSTED_ORIGINS = ['https://pelayo-sn-media.b-cdn.net/', 'https://jackson782.pythonanywhere.com/']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware"
]

ROOT_URLCONF = 'api.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'Jackson782.mysql.pythonanywhere-services.com',
        'USER': 'Jackson782',
        'PASSWORD': 'mysqldatabase&!',
        'NAME': 'Jackson782$default',
        'CHARSET': 'utf8',
    },
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = 'static/'

STATICFILES_DIRS = [

]

STATIC_ROOT =  BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    "https://pelayo-sn-media.b-cdn.net",
    "https://pelayo-social-network.web.app",
    "http://localhost:4200"
]

CORS_ALLOWED_PATHS = [
    r'^/media/gallery/',
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.educa.madrid.org'
#
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jalmeidaechevarria"
EMAIL_HOST_PASSWORD = "qwertyteclado&!1234M"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
}

AUTH_USER_MODEL = 'auth_app.User'

BACKEND_URL = 'https://jackson782.pythonanywhere.com'

ATOMIC_REQUESTS = True

cred = credentials.Certificate(BASE_DIR / "api" / "firebaseSecretKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'pelayo-social-network.appspot.com'})


