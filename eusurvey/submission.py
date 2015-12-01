import requests

from eusurvey import settings
from eusurvey.models import FormTree, PreSubmission
from lxml import html

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                   'Gecko/20100101 Firefox/40.1'),
}


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


def get_form_tree(url):
    response = requests.get(url, headers=HEADERS)
    tree = html.fromstring(response.content)
    return FormTree(tree=tree, response=response)


def post(url, data=None, cookies=None):
    response = requests.post(url, data, cookies=cookies, headers=HEADERS)
    return response
