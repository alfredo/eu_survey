import logging

from eusurvey.fields import importer
from eusurvey.poster import submission

logger = logging.getLogger(__name__)


def import_survey(url, update=False):
    try:
        update = True
        importer.process(url, is_update=update)
    except ValueError, e:
        logger.error(e)
    return True


def submit_surveys(url):
    try:
        submission.process(url, name='answers-export.csv')
    except ValueError, e:
        logger.error(e)
    return True
