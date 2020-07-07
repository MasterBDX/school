import os
import django_heroku

from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('SECRET_KEY')

# SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'assassinbd9@gmail.com'
EMAIL_HOST_PASSWORD = 'Baleead9@21112004'

SERVER_EMAIL = 'assassinbd9@gmail.com'

LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
                      },
            'filters': {
                'require_debug_false': {
                        '()': 'django.utils.log.RequireDebugFalse',
                }
            },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                #'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
                    },
                },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins',],
            'propagate': True,
            'level': 'DEBUG',
        },
        }
    }

DEBUG = False

ALLOWED_HOSTS = ['*']


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
DROPBOX_ROOT_PATH = os.environ.get('DROPBOX_ROOT_PATH')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True



django_heroku.settings(locals())