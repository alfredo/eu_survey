import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = lambda *x: os.path.join(BASE_DIR, *x)

DB_ROOT = here('db')
MASTER_FORM_NAME = 'master_form.html'

# Unique fields per form:
SPECIAL_FIELDS = (
    'survey.id',
    'language.code',
    'uniqueCode',
    'IdAnswerSet',
    'invitation',
    'participationGroup',
    'hfsubmit',
    'mode',
    'draftid',
    'newlang',
)


VERBOSE_FORMAT = '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s'

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
