import logging

from eusurvey.poster import constants


logger = logging.getLogger(__name__)


def is_valid_payload(payload):
    missing = set(constants.EXPECTED_KEYS) - set(payload.keys())
    missing = missing - set(constants.SPECIAL_FIELDS)
    if missing:
        logging.error('Missing fields: %s', missing)
        logging.error(payload)
        return False
    return True