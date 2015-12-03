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
    pattern = u'.//span[@class="mandatory"]/text()'
    return bool(question.xpath(pattern))


def get_label(field_element):
    """Determines the label for the field_element."""
    label_field = get(field_element.xpath('.//td/label'))
    return get(label_field.xpath('.//span[@class="answertext"]/text()'))


def get_question_title(section):
    pattern = './/div[@class="questiontitle"]/table/tr/td'
    container =  section.xpath(pattern)[1]
    return container.text_content()


def get_data_triggers(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    if not section.xpath(pattern):
        return []
    attrs = get(section.xpath(pattern)).attrib
    return filter(None, attrs['data-triggers'].split(';'))


def is_supplementary(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    return bool(section.xpath(pattern))
