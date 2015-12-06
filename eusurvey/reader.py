import requests

from eusurvey import database, settings
from eusurvey.models import FormTree
from lxml import html


def get_form_tree(url, use_cache=False):
    if use_cache:
        stream = database.read_file(settings.MASTER_FORM_NAME)
        response = None
    else:
        response = requests.get(url, headers=settings.HEADERS)
        database.save_stream(response.content, settings.MASTER_FORM_NAME)
        stream = response.content
    tree = html.fromstring(stream)
    return FormTree(tree=tree, response=response)
