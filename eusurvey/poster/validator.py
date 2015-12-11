import logging

from eusurvey.poster import constants

logger = logging.getLogger(__name__)


def get_expected_keys(tree):
    """Calculate the expected payload from the form tree."""
    field_list = set()
    pattern_list = [
        '//form//input',
        '//form//textarea',
    ]
    for pattern in pattern_list:
        for element in tree.xpath(pattern):
            if element.name:
                field_list.add(element.name)
    return field_list


def is_valid_payload(payload, survey_dict):
    EXPECTED_KEYS = get_expected_keys(survey_dict['form_tree'].tree)
    logger.debug('Total payload fields: `%s`', len(payload.keys()))
    logger.debug('Total expected fields: `%s`', len(EXPECTED_KEYS))
    missing = set(EXPECTED_KEYS) - set(payload.keys())
    missing = missing - set(constants.SPECIAL_FIELDS)
    if missing:
        logging.error('Missing fields: %s', missing)
        raise ValueError('Payload is invalid.')
    return True
