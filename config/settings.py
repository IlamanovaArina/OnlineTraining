import os
import sys
from datetime import timedelta
from pathlib import Path
from django.core.management.utils import get_random_secret_key

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = os.getenv('SECRET_KEY') or get_random_secret_key()

DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt',
    'rest_framework',
    # 'django.contrib.staticfiles',  # требуется для обслуживания файлов css/js интерфейса swagger
    'drf_yasg',
    'corsheaders',
    'django_celery_beat',

    'users',
    'materials',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

if os.getenv('TESTING') == '1':
    print("База данных определена как: sqlite3")
    print(str(BASE_DIR / 'test_db.sqlite3'), type(str(BASE_DIR / 'test_db.sqlite3')))
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'test_db.sqlite3'),  # Добавлен str() для преобразования Path в строку
            'TEST': {
                'NAME': str(BASE_DIR / 'test_db.sqlite3'),
            }
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv('POSTGRES_HOST'),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_PORT'),
#     }
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://redis:6379/1',
#     }
# }

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

# Настройки JWT-токенов
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Установите желаемый размер страницы
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
]

CORS_ALLOW_ALL_ORIGINS = False

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'logs.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         # Ваш логгер
#         __name__: {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }

# АПИ из стрип оплаты
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')

# Настройки для Celery
# URL-адрес брокера сообщений
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Часовой пояс для работы Celery
# CELERY_TIMEZONE = "Moscow"
CELERY_TIMEZONE = TIME_ZONE

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'materials.tasks.set_schedule',  # Путь к задаче
        'schedule': timedelta(days=1),  # Расписание выполнения задачи (например, каждые 10 минут)
    },
}
