import codecs
import logging
import os
import ConfigParser

from eusurvey import settings
from eusurvey.libs import csv_unicode as csv


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


def create_config(config_list, survey_path):
    SECTION = 'GENERAL'
    config = ConfigParser.RawConfigParser()
    config.add_section(SECTION)
    config_list.reverse()
    for key, value in config_list:
        config.set(SECTION, key, value)
    config_path = os.path.join(survey_path, 'config.cfg')
    with open(config_path, 'wb') as cfg_file:
        config.write(cfg_file)
    return config_path


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
    config_list = [
        ('form_id', survey['id']),
    ]
    config_path = create_config(config_list, survey_path)
    form_path = os.path.join(survey_path, 'source.html')
    save_stream(survey['form_tree'].stream, form_path)
    return {
        'survey_path': survey_path,
        'config_path': config_path,
        'form_path': form_path,
    }


def save_csv_file(file_path, row_list):
    with open(file_path, 'w') as stream:
        writer = csv.UnicodeWriter(stream)
        for row in row_list:
            writer.writerow(row)
    logging.debug('Saving CSV file: `%s`', file_path)
    return file_path


def complete_db(survey_dict, row_list):
    """Complates the missing details in the DB."""
    survey_path = survey_dict['survey_path']
    limesurvey_path = os.path.join(survey_path, 'limesurvey.txt')
    save_csv_file(limesurvey_path, row_list)
    # TODO: Create master csv MAP.
    return {
        'limesurvey_path': limesurvey_path,
    }
