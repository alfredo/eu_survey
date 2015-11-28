import codecs
import requests

from collections import namedtuple
from eusurvey.variables import PAYLOAD
from lxml import html
from urlparse import parse_qs

URL = 'https://ec.europa.eu/eusurvey/runner/Platforms/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
}

SPECIAL_FIELDS = (
    'survey.id',
    'language.code',
    'uniqueCode',
    'IdAnswerSet',
    'invitation',
    'participationGroup',
    'hfsubmit',
    'mode',
)


def get_special_fields(tree):
    fields = []
    for field in SPECIAL_FIELDS:
        path = '//input[@name="%s"]/@value' % field
        value = tree.xpath(path)
        fields.append((field, value))
    return dict(fields)


def save_output(stream, name='output.html'):
    with codecs.open(name, 'w', 'utf-8') as f:
        f.write(stream.decode('utf-8'))
    return f


def read_output(name="output.html"):
    with codecs.open(name, 'r', 'utf-8') as f:
        return f.read()


def post(url=URL, data=None, cookies=None):
    response = requests.post(url, data, cookies=cookies, headers=HEADERS)
    return response


PreSubmission = namedtuple('PreSubmission', ['cookies', 'payload'])


def prepare_submission(url):
    """Any steps required before the data can be sent."""
    response = requests.get(url, headers=HEADERS)
    tree = html.fromstring(response.content)
    payload = get_special_fields(tree)
    return PreSubmission(cookies=response.cookies, payload=payload)


SuccessResponse = namedtuple('SuccessResponse', ['uid', 'url'])


def get_success_response(tree):
    uid = tree.xpath('//div[@id="divThanksInner"]/@name')[0]
    url = tree.xpath('//a[@id="printButtonThanksInner"]/@href')[0]
    return SuccessResponse(uid=uid, url=url)


def send_submission(url, payload, pre_submission):
    response = post(url, data=payload, cookies=pre_submission.cookies)
    tree = html.fromstring(response.content)
    success_response = get_success_response(tree)
    # Backup response
    save_output(response.content, name='%s.html' % success_response.uid)
    return success_response


def run(url=URL):
    pre_submission = prepare_submission(url)
    # TODO: Capture user input (replace dummy_payload):
    dummy_payload = parse_qs(PAYLOAD)
    dummy_payload.update(pre_submission.payload)
    success_result = send_submission(url, dummy_payload, pre_submission)
    print success_result
    print "Done."
