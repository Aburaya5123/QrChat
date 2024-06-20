from .base import *
from validators import domain


CURRENT_DOMAIN_NAME = f"https://{os.environ.get('DOMAIN_NAME')}"

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = []

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', "")


if domain(DOMAIN_NAME):
    CSRF_TRUSTED_ORIGINS.append(f"https://{DOMAIN_NAME}")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.AccessControlMiddleware',
]


# Channel-Redis(webSocket-backend)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        "CONFIG": {
            "hosts": [(os.environ.get('REDIS_HOST_IP'), 6379)],
        },
    },
}


# Django-Redis(Celery-backend)
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST_IP')}:6379/0"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST_IP')}:6379/0",
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER_NAME'),
        'PASSWORD': os.environ.get('DATABASE_USER_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
}

GS_PROJECT_ID = os.environ.get("PROJECT_ID")
GS_BUCKET_NAME = os.environ.get("STATIC_BUCKET_NAME")

GS_QUERYSTRING_AUTH = False
GS_OBJECT_PARAMETERS = {"cache_control" : "no-cache, max-age=0"}


STATIC_ROOT = f"https://storage.googleapis.com/{os.environ.get('STATIC_BUCKET_NAME')}/"

MEDIA_ROOT = f"https://storage.googleapis.com/{os.environ.get('MEDIA_BUCKET_NAME')}/"