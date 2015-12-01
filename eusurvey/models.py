from collections import namedtuple

FormTree = namedtuple('FormResponse', ['tree', 'response'])

PreSubmission = namedtuple('PreSubmission', ['cookies', 'payload'])

SuccessResponse = namedtuple('SuccessResponse', ['uid', 'url'])

Field = namedtuple('Field', [
    'name',
    'label',
])


Form = namedtuple('Form', [
    'title',
    'sections',
])
