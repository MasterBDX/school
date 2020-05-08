import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))



# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True


DEBUG = False

ALLOWED_HOSTS = []


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
# DROPBOX_ROOT_PATH = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
