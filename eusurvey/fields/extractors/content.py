from eusurvey.fields.common import (
    to_str,
    get,
    get_inner_html,
    get_field_id,
    get_data_triggers,
)


TEXT_PATTERN = u'.//div[@class="text"]'

PATTERN_LIST = [
    u'.//div[contains(@class, "sectiontitle")]',
    u'.//div[@class="alignment-div"]',
    u'.//a[@class="visiblelink"]',
    TEXT_PATTERN,
]


def get_text_attributes(section):
    print to_str(section)
    _a = lambda x: section.attrib.get(x)
    attrs = ['id', 'data-id']
    field = dict([(k, _a(k)) for k in attrs])
    if 'data-dependencies' in section.attrib:
        dependencies = _a('data-dependencies').split(';')
    else:
        dependencies = None
    field['data-dependencies'] = dependencies
    field['type'] = 'textarea'
    return field


def clean_text(content):
    content = get_inner_html(content)
    return content.strip()


class Content(object):
    field = None
    field_type = 'content'
    is_supplementary = False
    field_id = None
    data_triggers = None

    def __init__(self, section):
        self.section = section

    def is_content(self):
        for pattern in PATTERN_LIST:
            result = self.section.xpath(pattern)
            if result:
                self.field = self.extract_content(self.section)
                return True
        return False

    def is_text(self):
        return self.section.xpath(TEXT_PATTERN)

    def extract_content(self, section):
        content = get(section)
        result = {
            'text': clean_text(content),
        }
        if self.is_text():
            # Add extra required fields for the content:
            self.field_id = get_field_id(section)
            self.data_triggers = get_data_triggers(section)
            extra_attrs = get_text_attributes(content)
            result.update(extra_attrs)
        return result

    def get_dependencies(self):
        return {
            'field_id': self.field_id,
            'triggers': self.data_triggers
        }


def extractor(section):
    content = Content(section)
    if content.is_content():
        return content
    return None
