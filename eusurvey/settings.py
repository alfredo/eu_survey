import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = lambda *x: os.path.join(BASE_DIR, *x)

DB_ROOT = here('db')
MASTER_FORM_NAME = 'master_form.html'

VERBOSE_FORMAT = '%(levelname)-5s %(asctime)s %(module)-9s %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'verbose': {
            'format': VERBOSE_FORMAT
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'eusurvey.libs.stream_handler.ColorStreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'eusurvey': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                   'Gecko/20100101 Firefox/40.1'),
}
