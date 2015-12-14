import logging

from lxml import etree

logger = logging.getLogger(__name__)


def to_str(element):
    result = etree.tostring(element, pretty_print=True)
    return result.replace('\t', ' ')


def get(element_list):
    """Validates there is a single element in the list."""
    if not len(element_list) == 1:
        for element in element_list:
            logger.error(to_str(element))
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
    label = get(label_field.xpath('.//span[@class="answertext"]'))
    remove_elements = (
        '<span class="answertext">',
        '</span>',
    )
    label_text = get_inner_html(label, remove_elements)
    return label_text


def get_inner_html(element, remove_elements):
    element_str =  to_str(element)
    for item in remove_elements:
        element_str = element_str.replace(item, '')
    return ''.join(element_str.splitlines())


def get_question_title(section):
    pattern = './/div[@class="questiontitle"]/table/tr/td'
    element = section.xpath(pattern)[1]
    remove_elements = (
        '<td style="width: 100%">',
        '</td>'
    )
    return get_inner_html(element, remove_elements)


def get_data_triggers(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    if not section.xpath(pattern):
        return []
    attrs = get(section.xpath(pattern)).attrib
    return filter(None, attrs['data-triggers'].split(';'))


def is_supplementary(section):
    pattern = './/div[contains(@class, "survey-element untriggered")]'
    return bool(section.xpath(pattern))


def get_field_id(section):
    """Extracts the id for the field:
    Format:
    <div class="survey-element 5" id="6251561" data-id="6251561">
    """
    pattern = './/div[contains(@class, "survey-element")]'
    field = section.xpath(pattern)
    if field:
        field = get(field)
        return field.attrib['id']
    return None


def get_help_text(section):
    pattern = './/div[@class="questionhelp"]'
    help_text = section.xpath(pattern)
    if help_text:
        element = get(help_text)
        remove_elements = (
            '<div class="questionhelp">',
            '</div>',
        )
        result = get_inner_html(element, remove_elements)
        return result if result else None
    return None


def get_limits(section):
    pattern = './/div[@class="limits"]'
    limits = section.xpath(pattern)
    if limits:
        element = get(limits)
        # This is removing the extra markup based in the current copy.
        # this will need further tweaking to make sure only the numbers are
        # passed on:
        remove_elements = (
            '<div class="limits">',
            '</div>',
            '<span class="charactercounter"></span>',
            ' character(s) maximum&#160;',
            ' characters will be accepted&#160;',
            'to',
            'Text of',
            'between',
            'and',
            'choices',
        )
        limits = get_inner_html(element, remove_elements)
        try:
            limit_list = [int(l) for l in limits.split()]
        except ValueError:
            logger.error('Invalid limit: `%s`', limits)
            return None
        if limit_list and len(limit_list) <= 2:
            return limit_list
        logger.error('Invalid limit: `%s`', limits)
    return None


def get_matrix_id(section):
    pattern = './/div[contains(@class, "survey-element")]'
    matrix = get(section.xpath(pattern))
    return matrix.attrib['id']
