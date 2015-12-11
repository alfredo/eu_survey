import logging

from eusurvey import content, database, query
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
    survey_dict = query.get_survey_dict(url)
    db_dict = database.init_db(survey_dict)
    if not db_dict:
        # Survey couldn't be created return an error.
        raise ValueError('Survey could not be created.')
    survey_dict.update(db_dict)
    form_tree = survey_dict['form_tree']
    page_list = get_form_pages(form_tree.tree)
    survey_list = []
    for page in page_list:
        fields = get_page_fields(form_tree.tree, page)
        survey_list.append((page, fields))
    # TODO: Activate this with a flag:
    #  renderer.render(survey_list)
    row_list = lime_importer.make_limesurvey_file(survey_list)
    database.complete_db(survey_dict, row_list)
    return True
