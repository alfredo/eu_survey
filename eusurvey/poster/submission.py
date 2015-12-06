import os
import requests

from eusurvey import settings
from eusurvey.libs import csv_unicode as csv
from eusurvey.models import PreSubmission
from eusurvey.poster import translator


def get_special_fields(tree):
    fields = []
    for field in settings.SPECIAL_FIELDS:
        path = '//input[@name="%s"]/@value' % field
        value = tree.xpath(path)
        fields.append((field, value))
    return dict(fields)


def prepare_submission(form_tree):
    """Any steps required before the data can be sent."""
    payload = get_special_fields(form_tree.tree)
    return PreSubmission(cookies=form_tree.response.cookies, payload=payload)


def post(url, data=None, cookies=None):
    response = requests.post(url, data, cookies=cookies, headers=settings.HEADERS)
    return response


def read_csv(name):
    stream_path = os.path.join(settings.DB_ROOT, name)
    with open(stream_path, 'r') as stream:
        for row in csv.UnicodeReader(stream):
            yield row


def process(name):
    submission_list = list(read_csv(name))
    row_map = translator.update_key_map(submission_list[0])
    assert False, row_map
    for i, row in enumerate(submission_list[1:]):
        payload = translator.prepare_payload(row, row_map)
        assert False, row
