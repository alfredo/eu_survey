import requests

from eusurvey import database, settings
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


def get_form_tree(url, use_cache=False):
    if use_cache:
        stream = database.read_file(settings.MASTER_FORM_NAME)
        response = None
    else:
        response = requests.get(url, headers=HEADERS)
        database.save_stream(response.content, settings.MASTER_FORM_NAME)
        stream = response.content
    tree = html.fromstring(stream)
    return FormTree(tree=tree, response=response)


def post(url, data=None, cookies=None):
    response = requests.post(url, data, cookies=cookies, headers=HEADERS)
    return response
