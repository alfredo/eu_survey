from lxml import etree


def to_str(element):
    result = etree.tostring(element, pretty_print=True)
    return result.replace('\t', ' ')


def get(element_list):
    """Validates there is a single element in the list."""
    if not len(element_list) == 1:
        raise ValueError(
            'Different number of elements than expected: `%s`' % element_list)
    return element_list[0]


def is_mandatory(question):
    """Determines if the question is mandatory."""
    pattern = u'.//span[@class="mandatory"]'
    pattern_list = list(question.xpath(pattern))
    return bool(pattern_list)


def get_label(field_element):
    """Determines the label for the field_element."""
    label_field = get(field_element.xpath('.//td/label'))
    return get(label_field.xpath('.//span[@class="answertext"]/text()'))


def get_question_title(section):
    pattern = './/div[@class="questiontitle"]/table/tr/td'
    element = section.xpath(pattern)[1]
    element_str =  to_str(element)
    remove_elements = (
        '<td style="width: 100%">',
        '</td>'
    )
    for item in remove_elements:
        element_str = element_str.replace(item, '')
    return ''.join(element_str.splitlines())


def get_data_triggers(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    if not section.xpath(pattern):
        return []
    attrs = get(section.xpath(pattern)).attrib
    return filter(None, attrs['data-triggers'].split(';'))


def is_supplementary(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    return bool(section.xpath(pattern))


def get_help_text(section):
    pattern = './/div[@class="questionhelp"]'
    help_text = section.xpath(pattern)
    if help_text:
        remove_elements = (
            '<div class="questionhelp">',
            '</div>',
        )
        help_text = get(section.xpath(pattern))
        element_str = to_str(help_text)
        for item in remove_elements:
            element_str = element_str.replace(item, '')
        return ''.join(element_str.splitlines())
    return None


def get_limits(section):
    pattern = './/div[@class="limits"]'
    if section.xpath(pattern):
        limits = get(section.xpath(pattern))
        return limits.text_content()
    return None


def get_matrix_id(section):
    pattern = './/div[contains(@class, "survey-element")]'
    matrix = get(section.xpath(pattern))
    return matrix.attrib['id']
