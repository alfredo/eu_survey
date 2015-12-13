import os
import logging
import requests

from eusurvey import database, query, settings
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
    """Wraper around to `POST` the form passing on the headers and cookies."""
    response = requests.post(
        url, data, cookies=cookies, headers=settings.HEADERS)
    return response


def get_success_response(tree):
    uid = tree.xpath('//div[@id="divThanksInner"]/@name')[0]
    url = tree.xpath('//a[@id="printButtonThanksInner"]/@href')[0]
    return SuccessResponse(uid=uid, url=url)


def send_submission(url, payload, pre_submission):
    """Sends the submission payload to the survey URL."""
    response = post(url, data=payload, cookies=pre_submission.cookies)
    filename = 'submissions/answer-%s.html' % payload[0]['id']
    database.save_file(response.content, name=filename)
    tree = html.fromstring(response.content)
    success_response = get_success_response(tree)
    return success_response


def get_submissions_dict(row_list):
    """Look up table using the first cell as the ID."""
    return {r[0]: r for r in row_list}


def get_sent_submissions(survey_dict):
    """Reads the database of processed submissions if anys."""
    file_path = os.path.join(survey_dict['survey_path'], 'submissions.csv')
    if os.path.exists(file_path):
        # Exausting it in case we need to re-iterate it:
        submission_list = list(database.read_csv_file(file_path))
        logger.info(
            'Found submission file with: `%s` rows', len(submission_list))
        submissions = get_submissions_dict(submission_list)
    else:
        submissions = {}
    return submissions


def get_submission_row(row, success_response):
    """Generates a submission row to be recorded in the DB."""
    assert False, row


def complete_payload(url, payload):
    # Each submission requires a cookie and a token.
    # this step is done by preparing the submision:
    tree = query.get_form_tree(url)
    pre_submission = prepare_submission(tree)
    payload.update(pre_submission.payload)
    return payload, pre_submission


def get_submission_queue(submission_list, existing_list):
    """Filters any non-procesable submission"""
    submission_queue = []
    for submission in submission_list[1:]:
        if submission and (submission not in existing_list):
            submission_queue.append(submission)
        else:
            logger.debug('Ignoring procesed submission: `%s`', submission)
    logger.debug('Found submissions: `%s`', len(submission_queue))
    return submission_queue


def save_sent_submissions(sent_submissions, survey_dict):
    logger.info('Saving sent submissions: `%s`', len(sent_submissions))
    file_path = os.path.join(survey_dict['survey_path'], 'submissions.csv')
    database.save_csv_file(file_path, sent_submissions.values())
    return sent_submissions


def get_export_csv_path(survey_path, name):
    """Returns the most likely file."""
    if name:
        return os.path.join(survey_path, name)
    # Try to findout a file that look like a survey:
    item_list = []
    for item in os.listdir(survey_path):
        if item.startswith('results-survey') and item.endswith('.csv'):
            # Format of the exported surveys:
            return os.path.join(survey_path, item)
    return None



def process(url, name, dry=True):
    survey_dict = query.get_survey_dict(url)
    export_path = get_export_csv_path(survey_dict['survey_path'], name)
    if (not export_path) or (not os.path.exists(export_path)):
        logger.error('Missing exported survey answers: `%s`', export_path)
        raise ValueError('Cannot submit survey.')
    submission_list = list(database.read_csv_file(export_path))
    row_map = translator.update_key_map(submission_list[0])
    sent_submissions = get_sent_submissions(survey_dict)
    submission_queue = get_submission_queue(
        submission_list, sent_submissions.keys())
    for i, row in enumerate(submission_queue):
        submission_id = row[0]
        logger.debug('Processing submission: `%s`', submission_id)
        partial_payload = translator.prepare_payload(row, row_map)
        if validator.is_valid_payload(partial_payload, survey_dict):
            payload, pre_submission = complete_payload(url, partial_payload)
            if dry:
                logger.info('Dry run. Valid row: `%s`.', submission_id)
                continue
            else:
                # Send submissions
                success_response = send_submission(
                    url, payload, pre_submission)
                submission_row = get_submission_row(row, success_response)
                sent_submissions[submission_id] = submission_row
                logger.info('Submission sent: `%s`' % success_response)
    # Update with database with processed submissions:
    return save_sent_submissions(sent_submissions, survey_dict)
