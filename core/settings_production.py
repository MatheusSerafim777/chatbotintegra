from core.settings import *  # noqa: F403

DEBUG = False

# Override DJANGO_VITE dev_mode to match production DEBUG setting
# This is necessary because DJANGO_VITE is evaluated at import time
DJANGO_VITE['default']['dev_mode'] = False  # noqa: F405

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django security checklist settings
# More details here: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security settings
# https://docs.djangoproject.com/en/dev/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

USE_HTTPS_IN_ABSOLUTE_URLS = True

# Update your allowed hosts and CSRF trusted origins here.
ALLOWED_HOSTS = [
    '*',
]
CSRF_TRUSTED_ORIGINS = [
    'https://chatbotintegracar.online',
    'https://www.chatbotintegracar.online',
]

LOG_DIR = BASE_DIR / 'logs'  # noqa: F405
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '[{asctime}] [{levelname}] [{name}] '
                '[PID:{process:d} TID:{thread:d}] '
                '{module}:{lineno:d} | {message}'
            ),
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': str(LOG_DIR / 'django.log'),
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'file_errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'verbose',
            'filename': str(LOG_DIR / 'errors.log'),
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file', 'file_errors'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file', 'file_errors'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
