import logging

from eusurvey.fields import importer
from eusurvey.poster import submission

logger = logging.getLogger(__name__)


def import_survey(url):
    try:
        importer.process(url)
    except ValueError, e:
        logger.error(e)
    return True


def submit_surveys(url):
    try:
        submission.process(url, name='answers-export.csv')
    except ValueError, e:
        logger.error(e)
    return True
