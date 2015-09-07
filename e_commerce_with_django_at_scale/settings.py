"""
Django settings for e_commerce_with_django_at_scale project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h^0(q5$a)j+&#v%s#dtni#r8^364q9w*9%xp3ai2msetxy%%9r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'e_commerce_with_django_at_scale',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'e_commerce_with_django_at_scale.urls'

WSGI_APPLICATION = 'e_commerce_with_django_at_scale.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Databases
DATABASES = {
    'default': {
        'NAME': 'e_commerce_with_django_at_scale',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'ENGINE': 'mysql_failover_backend',
        'FAILOVER_RETRIES': 3,
    },
    'read-replica-1-failing': {
        'NAME': 'e_commerce_with_django_at_scale',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': '8.8.8.8',
        'ENGINE': 'mysql_failover_backend',
        'OPTIONS': {
            'connect_timeout': 5,
        },
        'FAILOVER_MASTER': 'default',
    },
    'read-replica-2': {
        'NAME': 'e_commerce_with_django_at_scale',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'ENGINE': 'mysql_failover_backend',
        'OPTIONS': {
            'connect_timeout': 5,
        },
        'FAILOVER_MASTER': 'default',
    },
}

# Database Routers
DATABASE_ROUTERS = ['read_replica_router.ReadReplicaRouter']
READ_REPLICAS = ['read-replica-1-failing', 'read-replica-2']

# Caches
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': 'default',
        'LOCATION': 'default',
        'TIMEOUT': 900,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
