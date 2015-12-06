import logging

from eusurvey.fields.common import to_str, get as g
from eusurvey.fields.extractors import base

logger = logging.getLogger(__name__)


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
    field['type'] = 'text'
    return field


def get_field_labels(title_row):
    row_list = []
    for element in title_row.xpath('.//td'):
        row_list.append(element.text.strip())
    return row_list[1:]


def get_input_list(section):
    pattern = './/table[@class="tabletable"]/tbody/tr'
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


def get_matrix_id(section):
    pattern = './/div[contains(@class, "survey-element")]'
    matrix = g(section.xpath(pattern))
    return matrix.attrib['id']


class TableTableFieldExtractor(base.Extractor):
    field_type = 'tabletable'
    pattern = './/table[@class="tabletable"]'

    def extract_field(self, section):
        self.matrix_id = get_matrix_id(section)
        self.field_list = get_input_list(section)
