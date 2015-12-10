import logging

from eusurvey import content, reader
from eusurvey.fields import renderer
from eusurvey.fields.common import to_str, get
from eusurvey.fields.extractors import (
    radio,
    select,
    textarea,
    checkbox,
    tabletable,
    matrixtable,
)
from eusurvey.limesurvey import importer as lime_importer

logger = logging.getLogger(__name__)


EXTRACTOR_LIST = (
    radio.RadioFieldExtractor,
    select.SelectFieldExtractor,
    textarea.TextareaFieldExtractor,
    checkbox.CheckboxFieldExtractor,
    tabletable.TableTableFieldExtractor,
    matrixtable.MatrixRadioFieldExtractor,
)


def extract_element(section):
    for Extractor in EXTRACTOR_LIST:
        extractor = Extractor(section)
        if extractor.has_pattern():
            return extractor
    # Extract content:
    content_element = content.extractor(section)
    if content_element:
        return content_element
    logger.error('Extractor for section not found:\n %s', to_str(section))
    assert False, to_str(section)


def get_form_title(tree):
    """Gets the title of the form."""
    return tree.xpath('//div[@class="surveytitle"]/text()')[0]


def get_form_pages(tree):
    """Extracts the forms sections from the given tree."""
    IGNORED_PAGES = ['Submission']
    section_list = []
    for section in tree.xpath('//div[contains(@class, "pagebutton")]'):
        data_id = section.attrib['data-id']
        title = section.xpath('a/div/text()')[0].strip()
        html_id = section.xpath('a/@id')[0].strip()
        if title in IGNORED_PAGES:
            logger.info('Ignoring page: `%s`', title)
            continue
        section_list.append({
            'title': title,
            'id': html_id,
            'data_id': data_id
        })
    return section_list


def get_page_fields(tree, page):
    page_id = 'page%s' % page['id'].replace('tab', '')
    page_element = get(tree.xpath('.//div[@id="%s"]' % page_id))
    field_list = []
    for element in page_element.xpath('.//div[@class="elem_basic"]'):
        item = extract_element(element)
        field_list.append(item)
    return field_list


def process(url):
    form_tree = reader.get_form_tree(url, use_cache=True)
    title = get_form_title(form_tree.tree)
    page_list = get_form_pages(form_tree.tree)
    survey_list = []
    for page in page_list:
        fields = get_page_fields(form_tree.tree, page)
        survey_list.append((page, fields))
    lime_importer.make_limesurvey_file(survey_list)
    renderer.render(survey_list)
    return True
