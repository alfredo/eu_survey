import codecs
import logging
import os

from eusurvey import settings

logger = logging.getLogger(__name__)


def save_stream(stream, name):
    file_path = os.path.join(settings.DB_ROOT, name)
    logger.debug('Saving stream: `%s`', file_path)
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(stream.decode('utf-8'))
    return file_path


def read_file(name):
    file_path = os.path.join(settings.DB_ROOT, name)
    logger.debug('Reading stream: `%s`', file_path)
    with codecs.open(file_path, 'r', 'utf-8') as f:
        return f.read()
    raise ValueError('Something went wrong with: `%s`' % file_path)


def init_db(survey):
    """Prepares the storage for the given survey."""
    survey_path = os.path.join(settings.DB_ROOT, survey['name'])
    if os.path.exists(survey_path):
        logger.error(
            'Survey has already been imported: See: `%s`', survey_path)
        return False
    path_list = (
        survey_path,
        os.path.join(survey_path, 'submissions'),
    )
    for path in path_list:
        logger.debug('Directory created: `%s`', path)
        os.mkdir(path)
    return True
