"""
Django settings for demos project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a-lo$!0hfut#%%*6(xujio5u2t&e7bi3&=5de$#9ihx4s_ck1&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'adminactions',
    'background_task',
    #'grappelli_dynamic_navbar',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    #'control',
    'import_export',
    'django.contrib.humanize',
    'fontawesome',
    'geoposition',
    'colorfield',
    'inblensa',
    'realstate',
    #'arca',
    'rrhh',
    'base',
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

ROOT_URLCONF = 'demos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'demos.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'demos',
        'USER': 'postgres',
        'PASSWORD': 'ABC123#$',
        #'PASSWORD': 'N3wd3v3l0p',
        'HOST': 'localhost',
        #'HOST': 'demos.deltacopiers.com',
        'PORT': '5432',
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-NI'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# default uses locally shipped version at 'fontawesome/css/font-awesome.min.css'
FONTAWESOME_CSS_URL = '//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'  # absolute url

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyCqPdfjM76erNHpC9HR3azDso29bBX6L_c'

# For email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True

EMAIL_HOST = 'gator3004.hostgator.com'

EMAIL_HOST_USER = 'jose.garcia@metropolitanadistribucion.com'

# Must generate specific password for your app in [gmail settings][1]
EMAIL_HOST_PASSWORD = 'N3wd3v3l0p'

EMAIL_PORT = 465

# This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Variables para el envio por gmail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xangcastle@gmail.com'
EMAIL_HOST_PASSWORD = 'ABcq12!@'
EMAIL_PORT = 587

LOGIN_URL = '/admin/login/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.email.EmailAuth',
)

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    #'social_core.pipeline.user.create_user',
    'arca.pipeline.save_profile',
    #'social_core.pipeline.social_auth.associate_user',
    #'social_core.pipeline.social_auth.load_extra_data',
    #'social_core.pipeline.user.user_details',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '730334026573-r34fa81bs1tb9rljf9jss17p44jkt6fc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'e5AOZPmaqsOr4I8P7M7L8XYv'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/arca/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/arca/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/arca/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/arca/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/arca/'
SOCIAL_AUTH_INACTIVE_USER_URL = '/arca/'
