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
