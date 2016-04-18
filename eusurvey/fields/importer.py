import logging

from eusurvey import database, query
from eusurvey.fields.common import to_str, get
from eusurvey.fields.extractors import (
    radio,
    select,
    textarea,
    checkbox,
    tabletable,
    matrixtable,
    content,
    inputtext,
)
from eusurvey.limesurvey import importer as lime_importer, mapper

logger = logging.getLogger(__name__)


EXTRACTOR_LIST = (
    radio.RadioFieldExtractor,
    select.SelectFieldExtractor,
    textarea.TextareaFieldExtractor,
    checkbox.CheckboxFieldExtractor,
    tabletable.TableTableFieldExtractor,
    matrixtable.MatrixRadioFieldExtractor,
    inputtext.InputtextFieldExtractor,
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
    logger.error('Please add the extractor in `eusurvey.fields.importer` '
                 'before continue.')
    exit(2)


def get_form_pages(tree, language):
    """Extracts the forms sections from the given tree."""
    IGNORED_PAGES = ['Submission']
    section_list = []
    for section in tree.xpath('//div[contains(@class, "pagebutton")]'):
        data_id = section.attrib['data-id']
        title = section.xpath('a/div/text()')[0].strip()
        html_id = section.xpath('a/@id')[0].strip()
        if title in IGNORED_PAGES:
            logger.debug('Ignoring page: `%s`', title)
            continue
        section_list.append({
            'title': title,
            'id': html_id,
            'data_id': data_id,
            'language': language,
        })
    return section_list


def get_page_fields(tree, page):
    page_id = 'page%s' % page['id'].replace('tab', '')
    page_element = get(tree.xpath('.//div[@id="%s"]' % page_id))
    field_list = []
    for element in page_element.xpath('.//div[@class="elementwrapper"]'):
        item = extract_element(element)
        field_list.append(item)
    return field_list


def process_language(form_tree):
    language = form_tree.language
    survey_list = []
    page_list = get_form_pages(form_tree.tree, language)
    for page in page_list:
        # TODO add language to page fields. Stop hardcoding it.
        fields = get_page_fields(form_tree.tree, page)
        survey_list.append((page, fields))
    return survey_list


def process(url, is_update=False):
    survey_dict = query.get_survey_dict(url)
    # Prepare file structure:
    if is_update:
        logger.info(
            'Updating existing imported survey: `%s`', survey_dict['name'])
        db_dict = database.read_db(survey_dict)
    else:
        db_dict = database.init_db(survey_dict)
        if not db_dict:
            # Survey couldn't be created return an error.
            raise ValueError('Survey could not be created.')
    survey_dict.update(db_dict)
    # Extract fields for the original language:
    survey_list = process_language(survey_dict['form_tree'])
    # TODO: Process each translated survey and add ordered fields to the list:
    lime_dict = lime_importer.convert_survey_list(survey_list)
    survey_dict['limesurvey'] = lime_dict['full_list']
    survey_dict['limesurvey_map'] = mapper.create_mapper(lime_dict['questions'])
    database.complete_db(survey_dict)
    return True
