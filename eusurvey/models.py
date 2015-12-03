from collections import namedtuple


class RadioField(object):

    def __init__(self, question=None, mandatory=False, input_list=None):
        self.question = question
        self.mandatory = mandatory
        self.input_list = input_list


class SelectField(object):

    def __init__(self, question=None, mandatory=False, option_list=None):
        self.question = question
        self.mandatory = mandatory
        self.option_list = option_list


class TextareaField(object):

    def __init__(self, question=None, mandatory=False, textarea=None,
                 data_triggers=None, supplementary=False):
        self.question = question
        self.mandatory = mandatory
        self.textarea = textarea
        self.data_triggers = data_triggers


class CheckboxField(object):

    def __init__(self, question=None, mandatory=False, input_list=None):
        self.question = question
        self.mandatory = mandatory
        self.input_list = input_list


FormTree = namedtuple('FormResponse', ['tree', 'response'])

PreSubmission = namedtuple('PreSubmission', ['cookies', 'payload'])

SuccessResponse = namedtuple('SuccessResponse', ['uid', 'url'])


Form = namedtuple('Form', [
    'title',
    'sections',
    'formset_list',
])
