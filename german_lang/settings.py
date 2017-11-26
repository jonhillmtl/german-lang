"""
Django settings for template project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# TODO TEMPLATE-USER: change this
SECRET_KEY = 'awg@-psy34n$$5mbf_ay3y=%_a^@$u#m3d(uba-lh2g+a(-6&!'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO TEMPLATE-USER: change this
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_json_api',
    'api',
    'apps',
    'landing'
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

# TODO TEMPLATE-USER: you can rename the "template" folder to something else,
# but you need to change it here
ROOT_URLCONF = 'german_lang.urls'

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
                'german_lang.context_processors.jwt_token_processor'
            ],
        },
    },
]

# TODO TEMPLATE-USER: you can rename the "template" folder to something else,
# but you need to change it here
WSGI_APPLICATION = 'german_lang.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# REST framework

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'django_jwt_auth.backends.JSONWebTokenAuthenticationBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    )
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'django_jwt_auth.backends.JSONWebTokenAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
)

JWT_KEY = {
    "k": os.environ.get('JWT_KEY', None),
    "kty" : "oct"
}

if JWT_KEY["k"] is None:
    print("Use https://github.com/jonhillmtl/jwt-key-gen to generate a JWT_KEY")
    raise ValueError("You need to set JWT_KEY in your environment.")

JWT_ALG = "HS256"
JWT_ENCRYPTION_ALG = "A256KW"
JWT_ENCRYPTION_ENC = "A256CBC-HS512"

# TODO TEMPLATE-USER: does your service have a User store, or is it a User-less microservice?
# if it is userless, then leave this as True
# if not, set it to False
JWT_AUTH_NO_USER_STORE = False

# we are using django-rest-framework, so we need to return tuples from our Auth backend
JWT_AUTH_RETURN_TUPLES = True