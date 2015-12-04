import logging

from eusurvey.fields.common import (
    get_data_triggers,
    get_question_title,
    is_mandatory,
    is_supplementary,
)

logger = logging.getLogger(__name__)


class Extractor(object):
    question = None
    is_mandatory = False
    is_supplementary = False
    data_triggers = None

    def __init__(self, section):
        self.section = section

    def extract_components(self, section):
        self.question = get_question_title(section)
        self.is_mandatory = is_mandatory(section)
        self.is_supplementary = is_supplementary(section)
        self.data_triggers = get_data_triggers(section)

    def has_pattern(self):
        fields = self.section.xpath(self.pattern)
        has_pattern = bool(fields)
        if has_pattern:
            self.extract_field(self.section)
        return has_pattern
