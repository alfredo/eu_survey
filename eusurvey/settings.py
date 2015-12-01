import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = lambda *x: os.path.join(BASE_DIR, *x)

DB_ROOT = here('db')

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
