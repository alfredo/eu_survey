import os
import requests

from eusurvey import settings, reader
from eusurvey.libs import csv_unicode as csv
from eusurvey.models import PreSubmission, SuccessResponse
from eusurvey.poster import translator, validator
from lxml import html


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


def get_success_response(tree):
    uid = tree.xpath('//div[@id="divThanksInner"]/@name')[0]
    url = tree.xpath('//a[@id="printButtonThanksInner"]/@href')[0]
    return SuccessResponse(uid=uid, url=url)


def send_submission(url, payload, pre_submission):
    response = post(url, data=payload, cookies=pre_submission.cookies)
    tree = html.fromstring(response.content)
    success_response = get_success_response(tree)
    return success_response



def process(name, url):
    submission_list = list(read_csv(name))
    row_map = translator.update_key_map(submission_list[0])
    for i, row in enumerate(submission_list[1:]):
        payload = translator.prepare_payload(row, row_map)
        if validator.is_valid_payload(payload):
            # Each submission requires a cookie and a token.
            # this step is done by preparing the submision:
            tree = reader.get_form_tree(url)
            pre_submission = prepare_submission(tree)
            payload.update(pre_submission.payload)
            assert False, "VALID"
        assert False, "NOT VALID"
