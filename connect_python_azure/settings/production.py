import os

from connect_python_azure.settings.shared import *

# Reading App Service hostname from an environment variable for demo purposes.
app_service_host = os.environ.get('APP_SERVICE_NAME')
ALLOWED_HOSTS = [f"{app_service_host}.azurewebsites.net"]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Debug mode off in Production
DEBUG = False


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']


# Database - https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_PASSWORD = os.environ['DB_PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': f'{DB_USER}@{DB_HOST}',
        'PASSWORD': DB_PASSWORD,
        'HOST': f'{DB_HOST}.postgres.database.azure.com',
        'PORT': '',
    }
}
