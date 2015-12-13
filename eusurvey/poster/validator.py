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
    missing = set(EXPECTED_KEYS) - set(payload.keys())
    missing = missing - set(constants.SPECIAL_FIELDS)
    if missing:
        logging.error('Missing `%s` keys:\n`%s`', len(missing), missing)
        return False
    logging.info('Valid payload found. `%s` keys' % len(payload.keys()))
    return True
