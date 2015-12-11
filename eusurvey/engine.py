import logging

from eusurvey.fields import importer
from eusurvey.poster import submission

logger = logging.getLogger(__name__)


URL = 'https://ec.europa.eu/eusurvey/runner/Platforms/'


def import_survey(url):
    try:
        importer.process(url)
    except ValueError, e:
        logger.error(e)
    return True


def submit_surveys(name='results-survey.csv', url=URL):
    submission.process(name, url)
    return True
