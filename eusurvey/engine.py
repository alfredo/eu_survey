import logging

from eusurvey.fields import importer
from eusurvey.poster import submission
from eusurvey.limesurvey import mapper

logger = logging.getLogger(__name__)


def import_survey(url, update=False):
    try:
        importer.process(url, is_update=update)
    except ValueError, e:
        logger.error(e)
    return True


def submit_surveys(url, name=None, dry=False):
    try:
        submission.process(url, name=name, dry=dry)
    except ValueError, e:
        logger.error(e)
    return True


def map_survey(url):
    try:
        mapper.process(url, name='untranslated.csv')
    except ValueError, e:
        logger.error(e)
    return True
