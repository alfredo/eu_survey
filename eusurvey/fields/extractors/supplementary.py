import logging

from eusurvey.fields.common import (
    get as g,
    get_data_triggers,
    get_question_title,
    is_mandatory,
    to_str,
)

logger = logging.getLogger(__name__)


def get_textarea(section):
    textarea = g(section.xpath('.//textarea'))
    _a = lambda x: textarea.attrib.get(x)
    attrs = ['id', 'name', 'data-id', 'data-dependencies', 'value']
    field = dict([(k, _a(k)) for k in attrs])
    field['type'] = 'textarea'
    return field


class SupplementaryFieldExtractor(object):

    name = 'Supplementary extractor'

    def __init__(self, section):
        self.section = section

    def validate(self):
        """Determines if the section is part of this extractor"""
        pattern = './/div[contains(@class, "survey-element untriggered")]'
        return bool(self.section.xpath(pattern))

    def extract(self):
        question = get_question_title(self.section)
        mandatory = is_mandatory(self.section)
        triggers = get_data_triggers(self.section)
        textarea = get_textarea(self.section)
        return True
