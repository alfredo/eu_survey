from eusurvey.fields.common import get as g, to_str
from eusurvey.fields.extractors import base


def get_option_list(section):
    option_list = []
    for option in section.xpath('.//option'):
        _a = lambda x: option.attrib.get(x)
        attrs = ['id', 'data-id', 'value']
        field = dict([(k, _a(k)) for k in attrs])
        field['text'] = option.text.strip() if option.text else None
        if 'data-dependencies' in option.attrib:
            dependencies = _a('data-dependencies').split(';')
        else:
            dependencies = None
        field['data-dependencies'] = dependencies
        field['type'] = 'option'
        option_list.append({
            'label': field['text'],
            'input': field,
        })
    return option_list


def get_field(section):
    select = g(section.xpath('.//select'))
    _a = lambda x: select.attrib.get(x)
    attrs = ['id', 'data-id', 'name']
    field = dict([(k, _a(k)) for k in attrs])
    return field


class SelectFieldExtractor(base.Extractor):
    field_type = 'select'
    pattern = './/div/select'

    def extract_field(self, section):
        self.field = get_field(section)
        self.option_list = get_option_list(section)
