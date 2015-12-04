from eusurvey.fields.extractors import base
from eusurvey.models import TextareaField
from eusurvey.fields.common import (
    get as g,
)


def get_textarea(section):
    textarea = g(section.xpath('.//textarea'))
    _a = lambda x: textarea.attrib.get(x)
    attrs = ['id', 'name', 'data-id', 'data-dependencies', 'value']
    field = dict([(k, _a(k)) for k in attrs])
    field['type'] = 'textarea'
    return field


class TextareaFieldExtractor(base.Extractor):
    field_type = 'textarea'
    pattern = './/div/textarea'

    def extract(self):
        self.textarea = get_textarea(self.section)
        return TextareaField(
            question=self.question, mandatory=self.mandatory,
            textarea=self.textarea, data_triggers=self.data_triggers,
            supplementary=self.supplementary)
