import os

import codecs

from eusurvey import settings


def save_output(stream, name='output.html'):
    file_path = os.path.join(settings.DB_ROOT, name)
    assert False, file_path
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(stream.decode('utf-8'))
    return f


def read_output(name="output.html"):
    file_path = os.path.join(settings.DB_ROOT, name)
    with codecs.open(file_path, 'r', 'utf-8') as f:
        return f.read()
