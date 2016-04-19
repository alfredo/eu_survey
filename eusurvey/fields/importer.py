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
    """Extracts the limesurvey fields from the given form_tree.

    The form_tree contains description of the language it is in."""
    language = form_tree.language.lower()
    survey_list = []
    page_list = get_form_pages(form_tree.tree, language)
    for page in page_list:
        fields = get_page_fields(form_tree.tree, page)
        survey_list.append((page, fields))
    result = lime_importer.convert_survey_list(survey_list, language)
    return result


def process(url, is_update=False):
    """Main function to ingest the EUsurvey into a limesurvey format."""
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
    lime_dict = process_language(survey_dict['form_tree'])
    # Prepare limesurvey output:
    # Use main form_tree to determine configuration:
    limesurvey_tuples = lime_importer.get_survey_configuration(
        survey_dict['form_tree'])
    # Add all the configuration fields:
    limesurvey_tuples += lime_dict['full_list']
    for form_tree in survey_dict['translations']:
        logger.debug('Processing survey in `%s`.', form_tree.language)
        translated_lime_dict = process_language(form_tree)
        limesurvey_tuples += translated_lime_dict['full_list']
    survey_dict['limesurvey'] = limesurvey_tuples
    # Create a manual map to the default questions:
    survey_dict['limesurvey_map'] = mapper.create_mapper(lime_dict['questions'])
    database.complete_db(survey_dict)
    return True
