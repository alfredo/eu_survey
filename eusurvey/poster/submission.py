import os
import logging
import requests

from eusurvey import database, query, settings, reader
from eusurvey.models import PreSubmission, SuccessResponse
from eusurvey.poster import constants, translator, validator
from lxml import html

logger = logging.getLogger(__name__)


def get_special_fields(tree):
    fields = []
    for field in constants.SPECIAL_FIELDS:
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


def get_success_response(tree):
    uid = tree.xpath('//div[@id="divThanksInner"]/@name')[0]
    url = tree.xpath('//a[@id="printButtonThanksInner"]/@href')[0]
    return SuccessResponse(uid=uid, url=url)


def send_submission(url, payload, pre_submission):
    response = post(url, data=payload, cookies=pre_submission.cookies)
    tree = html.fromstring(response.content)
    filename = 'submissions/id-%s.html' % payload[0]['id']
    database.save_file(response.content, name=filename)
    success_response = get_success_response(tree)
    return success_response


def process(url, name):
    survey_dict = query.get_survey_dict(url)
    export_path = os.path.join(survey_dict['survey_path'], name)
    if not os.path.exists(export_path):
        logger.error('Missing exported survey answers: `%s`', export_path)
        raise ValueError('Cannot submit survey.')
    submission_list = list(database.read_csv_file(export_path))
    row_map = translator.update_key_map(submission_list[0])
    for i, row in enumerate(submission_list[1:]):
        payload = translator.prepare_payload(row, row_map)
        if validator.is_valid_payload(payload, survey_dict):
            # Each submission requires a cookie and a token.
            # this step is done by preparing the submision:
            tree = reader.get_form_tree(url)
            pre_submission = prepare_submission(tree)
            payload.update(pre_submission.payload)
            # Stop here to avoid sending the submission:
            assert False, "Submission stopped."
            # TODO: flags to stop the submission.
            success_response = send_submission(url, payload, pre_submission)
            logger.info(success_response)
            # Short circuit
            return True
        assert False, "NOT VALID"
