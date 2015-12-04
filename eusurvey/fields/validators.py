import logging

from eusurvey import settings
from lxml import etree

logger = logging.getLogger(__name__)

_str = etree.tostring


def validate_special_field(element):
    """Determines if the field is a valid field."""
    if element.tag == 'input' and element.type == 'hidden':
        if element.name in settings.SPECIAL_FIELDS or (not element.name):
            raise ValueError('Special field found `%s`' % element)
    return True


IGNORED_CLASSES = [
    'right-area',
    'surveytitle',
    'well',
    'linkstitle',
    'download-survey-pdf-dialog-spinner',
    'download-survey-pdf-dialog-error'
]


def validate_reserved_div(element):
    """Determines if the div is reserved."""
    if (element.tag == 'div') and ('class' in element.attrib):
        if element.attrib['class'] in IGNORED_CLASSES:
            raise ValueError(
                'Reserved `div` found `%s`-`%s`' %
                (element.attrib['class'], element))
    return True


def validate_invalid_tags(element):
    """Determines if the tag should be ignored"""
    if element.tag in ['br']:
        raise ValueError('Invalid tag found `%s`' % element.tag)
    return True


def is_valid_element(element):
    """Determines if the element shoud should be parsed."""
    filter_callable_list = [
        validate_invalid_tags,
        validate_special_field,
        validate_reserved_div,
    ]
    for filter_callable in filter_callable_list:
        try:
            filter_callable(element)
        except ValueError, e:
            logger.debug('Ignoring %s', e)
            return False
    return True
