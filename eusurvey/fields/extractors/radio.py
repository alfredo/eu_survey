import logging

from eusurvey.fields.extractors import base
from eusurvey.fields.common import (
    get as g,
    get_label,
)

logger = logging.getLogger(__name__)


def get_input(element):
    element = g(element.xpath('.//td/input'))
    _a = lambda x: element.attrib.get(x)
    attrs = ['id', 'name', 'value', 'data-id']
    field = dict([(k, _a(k)) for k in attrs])
    if 'data-dependencies' in element.attrib:
        dependencies = _a('data-dependencies').split(';')
    else:
        dependencies = None
    field['data-dependencies'] = dependencies
    field['type'] = 'radio'
    return field


def get_input_list(section):
    input_list = []
    for element in section.xpath('.//table[@class="answers-table"]/tr'):
        input_list.append({
            'label': get_label(element),
            'input': get_input(element),
        })
    return input_list


class RadioFieldExtractor(base.Extractor):
    field_type = 'radio'
    pattern = './/input[@type="radio"]'

    def extract_field(self, section):
        self.input_list = get_input_list(section)
