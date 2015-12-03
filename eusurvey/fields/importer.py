import logging

from eusurvey import submission, models
from eusurvey.fields import validators
from eusurvey.fields.common import to_str
from eusurvey.fields.extractors import (
    radio,
    select,
    textarea,
    checkbox,
)

logger = logging.getLogger(__name__)

from lxml import etree


IGNORED_CLASS = ['surveytitle']

_str = etree.tostring


def _get(element_list, expected=1):
    """Validates there is a single element in the list."""
    if not len(element_list) == expected:
        raise ValueError(
            'Different number of elements than expected: `%s`' % element_list)
    return element_list[0]


EXTRACTOR_LIST = (
    radio.RadioFieldExtractor,
    select.SelectFieldExtractor,
    textarea.TextareaFieldExtractor,
    checkbox.CheckboxFieldExtractor,
)


def extract_formset(section):
    if not validators.is_fields_section(section):
        return None
    for Extractor in EXTRACTOR_LIST:
        extractor = Extractor(section)
        if extractor.has_pattern():
            return extractor
    logger.error('Extractor for section not found:\n %s', to_str(section))
    assert False, "Missing"


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
    tree = submission.get_form_tree(url, use_cache=True)
    title = get_form_title(tree.tree)
    sections = get_form_sections(tree.tree)
    form_elements = get_form_elements(tree.tree)
    formset_list = []
    for element in form_elements:
        # Ignore non valid elements:
        if not validators.is_valid_element(element):
            continue
        formset = extract_formset(element)
        if not formset:
            continue
        formset_list.append(formset)
    return models.Form(**{
        'title': title,
        'sections': sections,
        'formset_list': formset_list,
    })
