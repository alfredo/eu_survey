import logging

from eusurvey import submission, models
from eusurvey.fields import validators

logger = logging.getLogger(__name__)

from lxml import etree


IGNORED_CLASS = ['surveytitle']

_str = etree.tostring


def extract_fields(section):
    if not validators.is_fields_section(section):
        return None
    # TODO: Extract fields from this section:
    import ipdb; ipdb.set_trace()
    return models.Field(name='', label='')


def get_form_elements(tree):
    """Extracts the fields containers."""
    return tree.xpath('//form/div/div/div')


def get_form_title(tree):
    """Gets the title of the form."""
    # <div class="surveytitle">
    return tree.xpath('//div[@class="surveytitle"]/text()')[0]


def get_form_sections(tree):
    """Extracts the forms sections from the given tree."""
    section_list = []
    for section in tree.xpath('//div[contains(@class, "pagebutton")]'):
        data_id = section.attrib['data-id']
        title = section.xpath('a/div/text()')[0].strip()
        html_id = section.xpath('a/@id')[0].strip()
        section_list.append((data_id, {
            'title': title,
            'html_id': html_id,
        }))
    return section_list


def process(url):
    tree = submission.get_form_tree(url)
    title = get_form_title(tree.tree)
    sections = get_form_sections(tree.tree)
    form_elements = get_form_elements(tree.tree)
    for element in form_elements:
        # Ignore non valid elements:
        if not validators.is_valid_element(element):
            continue
        print '*' * 30
        fields = extract_fields(element)
        if not fields:
            continue
    assert False, "ff"
    return models.Form(**{
        'title': title,
        'sections': sections,
    })
