"""
Django settings for the config project.

This file controls:
- Installed apps
- Database connection
- Security, static files, middleware, etc.
"""

from pathlib import Path

# Base directory of the project (folder that contains manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# WARNING: keep the secret key private in real projects (use env variables)
SECRET_KEY = 'django-insecure-change-this-in-production-djangoFileTTH'

# Debug mode shows detailed errors — turn OFF in production
DEBUG = True

# Hosts allowed to serve this app
ALLOWED_HOSTS = ['*']


# ------------------------------------------------------------
# INSTALLED APPS
# Each app adds features. Django only loads apps listed here.
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin dashboard at /admin
    'django.contrib.auth',           # User authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',                # Django REST Framework (for APIs)

    # Our app
    'api',                           # The Notes API app we created
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ------------------------------------------------------------
# DATABASE — PostgreSQL (running in the "db" Docker container)
# HOST must be "db" (the service name in docker-compose.yml),
# not "localhost", because containers talk to each other by service name.
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'user',
        'PASSWORD': 'secret',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation (used when creating users)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# URL prefix for static files (CSS, JS, images)
STATIC_URL = 'static/'

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Optional: basic DRF settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Open API for learning (lock later)
    ]
}
