from eusurvey import database, reader
from eusurvey.fields import importer
from eusurvey.models import SuccessResponse
from eusurvey.poster import submission
from eusurvey.variables import PAYLOAD
from lxml import html
from urlparse import parse_qs


URL = 'https://ec.europa.eu/eusurvey/runner/Platforms/'


def get_success_response(tree):
    uid = tree.xpath('//div[@id="divThanksInner"]/@name')[0]
    url = tree.xpath('//a[@id="printButtonThanksInner"]/@href')[0]
    return SuccessResponse(uid=uid, url=url)


def send_submission(url, payload, pre_submission):
    response = submission.post(url, data=payload, cookies=pre_submission.cookies)
    tree = html.fromstring(response.content)
    success_response = get_success_response(tree)
    return success_response


def run(url=URL):
    tree = reader.get_form_tree(url)
    pre_submission = submission.prepare_submission(tree)
    # TODO: Capture user input (replace dummy_payload):
    dummy_payload = parse_qs(PAYLOAD)
    dummy_payload.update(pre_submission.payload)
    # success_result = send_submission(url, dummy_payload, pre_submission)
    # Backup response
    # database.save_output(response.content, name='%s.html' % success_response.uid)
    result = database.read_output(
        name='bf31722d-a7d2-4a16-b3c8-b0af9c34d598.html')
    assert False, result
    # print success_result
    print "Done."


def import_fields(url=URL):
    """Imports the given form fields"""
    importer.process(url)
    return True


def submit_surveys(name='results-survey.csv'):
    submission.process(name)
    return True
