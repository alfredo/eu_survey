from eusurvey.fields import importer
from eusurvey.poster import submission


URL = 'https://ec.europa.eu/eusurvey/runner/Platforms/'


def import_survey(url):
    importer.process(url)
    return True


def submit_surveys(name='results-survey.csv', url=URL):
    submission.process(name, url)
    return True
