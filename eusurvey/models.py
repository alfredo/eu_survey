from collections import namedtuple

FormTree = namedtuple('FormResponse', ['tree', 'response'])

PreSubmission = namedtuple('PreSubmission', ['cookies', 'payload'])

SuccessResponse = namedtuple('SuccessResponse', ['uid', 'url'])

Label = namedtuple('Label', [
    'text',
    'pk',
])

Field = namedtuple('Field', [
    'label',
    'widget',
])

FormSet = namedtuple('FormSet', [
    'question',
    'field_list',
    'is_mandatory',
])

Form = namedtuple('Form', [
    'title',
    'sections',
    'formset_list',
])
