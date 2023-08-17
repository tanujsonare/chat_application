from .settings import *
from decouple import config


SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = ["chatapplication-production-e945.up.railway.app"]

CSRF_TRUSTED_ORIGINS = ['chatapplication-production-e945.up.railway.app']

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PORT': config('DATABASE_PORT'),
        'HOST': config('DATABASE_HOST'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'OPTIONS': {'sslmode': 'require'},
    }
}
