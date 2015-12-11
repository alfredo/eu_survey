import requests

from eusurvey import settings
from eusurvey.models import FormTree
from lxml import html


def get_form_tree(url):
    """Reads the form URL."""
    response = requests.get(url, headers=settings.HEADERS)
    tree = html.fromstring(response.content)
    return FormTree(tree=tree, response=response, stream=response.content)
