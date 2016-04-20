import os
import requests
import logging

from eusurvey import settings
from eusurvey.fields.common import get, get_inner_html
from eusurvey.models import FormTree
from slugify import slugify
from lxml import html
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode

logger = logging.getLogger(__name__)


def clean_url(url, params):
    url_parts = list(urlparse(url))
    querystring = parse_qs(url_parts[4])
    if params:
        querystring.update(params)
        url_parts[4] = urlencode(querystring)
    return urlunparse(url_parts)


def get_form_tree(url, params=None):
    """Reads the form URL."""
    cleaned_url = clean_url(url, params)
    response = requests.get(cleaned_url, headers=settings.HEADERS)
    tree = html.fromstring(response.content)
    return FormTree(tree=tree, response=response, stream=response.content,
                    language=tree.attrib.get('lang'))


def get_form_title(tree):
    """Gets the title of the form."""
    title = get(tree.xpath('//div[@class="surveytitle"]'))
    title_text = get_inner_html(title)
    return title_text


def get_language_list(tree, ignore_list=None):
    elements = tree.xpath('.//select[@id="langSelectorRunner"]/option')
    language_list = [e.attrib.get('value') for e in elements]
    if ignore_list:
        language_list = filter(lambda l: l not in ignore_list, language_list)
    return language_list


def get_survey_name(url):
    """Determines the survey name."""
    return slugify(url, only_ascii=True)


def get_survey_dict(url, with_translations=True):
    """Extracts the survey information."""
    form_tree = get_form_tree(url)
    name = get_survey_name(url)
    if with_translations:
        language_list = get_language_list(
            form_tree.tree, ignore_list=[form_tree.language])
        _lang_form = lambda l: get_form_tree(url, params={'surveylanguage': l})
        translations = [_lang_form(l) for l in language_list]
    else:
        translations = []
    return {
        'id': None,
        'url': url,
        'name': name,
        'title': get_form_title(form_tree.tree),
        'form_tree': form_tree,
        'translations': translations,
        'survey_path': os.path.join(settings.DB_ROOT, name),
    }
