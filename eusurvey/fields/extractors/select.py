from eusurvey.fields.extractors import base


def get_option_list(section):
    option_list = []
    for option in section.xpath('.//option'):
        _a = lambda x: option.attrib.get(x)
        attrs = ['id', 'name', 'data-id', 'data-dependencies', 'value']
        field = dict([(k, _a(k)) for k in attrs])
        field['text'] = option.text.strip() if option.text else None
        field['type'] = 'option'
        option_list.append(field)
    return option_list


class SelectFieldExtractor(base.Extractor):
    field_type = 'select'
    pattern = './/div/select'

    def extract_field(self):
        self.option_list = get_option_list(self.section)
