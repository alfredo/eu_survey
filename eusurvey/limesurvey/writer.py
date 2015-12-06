import os
import logging

from eusurvey import settings
from eusurvey.libs import csv_unicode as csv


logger = logging.getLogger(__name__)


def save(row_list):
    path = os.path.join(settings.DB_ROOT, 'limesurvey-form.txt')
    with open(path, 'w') as stream:
        writer = csv.UnicodeWriter(stream)
        for row in row_list:
            writer.writerow(row)
    logger.info('LimeSurvey CSV importable form saved in: `%s`' % path)
    return path
