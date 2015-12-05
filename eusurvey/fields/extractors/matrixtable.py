from eusurvey.fields.common import get as g, to_str
from eusurvey.fields.extractors import base


def get_field_labels(title_row):
    row_list = []
    for element in title_row.xpath('.//td'):
        text = element.text_content() if element.text_content() else ''
        row_list.append(text.strip())
    return row_list[1:]


def get_input(cell):
    element = g(cell.xpath('.//input'))
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
    pattern = './/table[contains(@class, "matrixtable")]/tr'
    row_list = list(section.xpath(pattern))
    field_labels = get_field_labels(row_list[0])
    input_list = []
    for i, element in enumerate(row_list[1:]):
        cell_list = list(element.xpath('.//td'))
        name = cell_list[0].text_content().strip()
        field_row = []
        for label, cell in zip(field_labels, cell_list[1:]):
            field_row.append({
                'label': label,
                'input': get_input(cell),
            })
        # Record name of the row and fields:
        input_list.append((name, field_row))
    return input_list


class MatrixRadioFieldExtractor(base.Extractor):
    field_type = 'matrixtable'
    pattern = './/table[contains(@class, "matrixtable")]'

    def extract_field(self, section):
        self.field_list = get_input_list(section)
