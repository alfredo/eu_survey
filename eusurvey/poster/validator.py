from urlparse import parse_qs

from eusurvey.variables import PAYLOAD
from eusurvey.poster import constants

def is_valid_payload(payload):
    assert False, set(constants.EXPECTED_KEYS) - set(payload.keys())

