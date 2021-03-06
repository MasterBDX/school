from easy_thumbnails.conf import Settings as thumbnail_settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

ADMINS = [('MasterBDX', 'masterbdxteam@gmail.com')]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_REDIRECT_URL = '/accounts/login/'

DEFENDER_REDIS_URL = os.environ.get('REDIS_URL')

# Django Defender Settings
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_COOLOFF_TIME = 120
DEFENDER_LOCKOUT_TEMPLATE = 'accounts/register.html'

MAIN_EMAIL = DEFAULT_FROM_EMAIL

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'debug_toolbar',
    'rest_framework',
    'crispy_forms',
    'defender',
    'django_summernote',
    'django_countries',
    'easy_thumbnails',
    'image_cropping',


    # my apps
    'accounts',
    'main',
    'posts',
    'school_tables',
    'students',
]

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


COUNTRIES_OVERRIDE = {
    'IL': None,
}


SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '400px',
        'toolbar': [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['font', ['strikethrough', 'superscript', 'subscript']],
            ['fontsize', ['fontname', 'fontsize', 'fontsizeunit']],
            ['color', ['forecolor', 'backcolor', 'color']],
            ['para', ['style', 'ul', 'ol', 'paragraph', 'height']],

            ['misc', ['fullscreen', 'codeview', 'print', 'help', 'undo', 'redo']],
            ['insert', ['picture', 'video', 'link', 'table', 'hr']]
        ],
    },
    'js': (
        '/static/summernote-ext-print.js',
    ),
    'js_for_inplace': (
        '/static/summernote-ext-print.js',
    ),
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
    ),
    'css_for_inplace': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
    ),
    'codemirror': {
        'theme': 'base16-dark',
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
    },
    'lazy': False,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'golden_pen.middleware.LangSessionMiddletware'
]

SITE_ID=1


ROOT_URLCONF = 'golden_pen.urls'

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
                'main.context_processors.school_name'

            ],
        },
    },
]

WSGI_APPLICATION = 'golden_pen.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'golden_pen.validators.IsAsciiValidator'},
    {'NAME': 'golden_pen.validators.MinimumLengthValidator'},
    {'NAME': 'golden_pen.validators.NumberValidator'},
    {'NAME': 'golden_pen.validators.UppercaseValidator', },
    {'NAME': 'golden_pen.validators.LowercaseValidator', },
    {'NAME': 'golden_pen.validators.SymbolValidator', },
]


# Django Defender Settings
DEFENDER_LOGIN_FAILURE_LIMIT = 3
DEFENDER_COOLOFF_TIME = 120
DEFENDER_LOCKOUT_TEMPLATE = 'accounts/register.html'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = '/static/'



LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
