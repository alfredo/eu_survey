from eusurvey.fields.extractors import base
from eusurvey.fields.common import (
    get as g,
)


def get_textarea(section):
    textarea = g(section.xpath('.//textarea'))
    _a = lambda x: textarea.attrib.get(x)
    attrs = ['id', 'name', 'data-id', 'value']
    field = dict([(k, _a(k)) for k in attrs])
    if 'data-dependencies' in textarea.attrib:
        dependencies = _a('data-dependencies').split(';')
    else:
        dependencies = None
    field['data-dependencies'] = dependencies
    field['type'] = 'textarea'
    return field


class TextareaFieldExtractor(base.Extractor):
    field_type = 'textarea'
    pattern = './/div/textarea'

    def extract_field(self, section):
        self.textarea = get_textarea(section)
