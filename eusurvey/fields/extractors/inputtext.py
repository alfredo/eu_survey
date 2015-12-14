from eusurvey.fields.extractors import base
from eusurvey.fields.common import (
    get as g,
)


def get_inputtext(section):
    inputtext = g(section.xpath('.//input[@type="text"]'))
    _a = lambda x: inputtext.attrib.get(x)
    attrs = ['id', 'name', 'data-id', 'value']
    field = dict([(k, _a(k)) for k in attrs])
    if 'data-dependencies' in inputtext.attrib:
        dependencies = _a('data-dependencies').split(';')
    else:
        dependencies = None
    field['data-dependencies'] = dependencies
    field['type'] = 'inputtext'
    return field


class InputtextFieldExtractor(base.Extractor):
    field_type = 'inputtext'
    pattern = './/input[@type="text"]'

    def extract_field(self, section):
        self.field = get_inputtext(section)
