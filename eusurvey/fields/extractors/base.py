import logging

from eusurvey.fields.common import (
    get_data_triggers,
    get_question_title,
    get_help_text,
    get_field_id,
    get_limits,
    is_mandatory,
    is_supplementary,
)

logger = logging.getLogger(__name__)


class Extractor(object):
    question = None
    is_mandatory = False
    is_supplementary = False
    data_triggers = None
    field_list = None
    field = None
    option_list = None
    help_text = None
    limits = None

    def __init__(self, section):
        self.section = section

    def extract_components(self, section):
        self.question = get_question_title(section)
        self.is_mandatory = is_mandatory(section)
        self.is_supplementary = is_supplementary(section)
        self.data_triggers = get_data_triggers(section)
        self.field_id = get_field_id(section)
        self.help_text = get_help_text(section)
        self.limits = get_limits(section)

    def has_pattern(self):
        fields = self.section.xpath(self.pattern)
        has_pattern = bool(fields)
        if has_pattern:
            self.extract_components(self.section)
            self.extract_field(self.section)
        return has_pattern

    def get_dependencies(self):
        return {
            'field_id': self.field_id,
            'triggers': self.data_triggers
        }
