from collections import namedtuple


FormTree = namedtuple(
    'FormResponse',
    ['tree', 'response', 'stream', 'language']
)

PreSubmission = namedtuple('PreSubmission', ['cookies', 'payload'])

SuccessResponse = namedtuple('SuccessResponse', ['uid', 'url'])


Form = namedtuple('Form', [
    'title',
    'sections',
    'formset_list',
])
