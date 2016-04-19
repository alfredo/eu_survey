import logging

from eusurvey.limesurvey import (
    constants,
    common,
    postprocessor,
)
from eusurvey.limesurvey.fields import (
    content,
    radio,
    textarea,
    select,
    checkbox,
    tabletable,
    matrixtable,
    inputtext,
)

logger = logging.getLogger(__name__)


def get_settings_rows(total):
    settings_rows = []
    for row in constants.GLOBAL_SETTINGS:
        missing = common.get_missing(row, total)
        full_row = list(row) + missing
        settings_rows.append(full_row)
    return settings_rows


def get_local_settings_rows(total, language):
    settings_rows = []
    for row in constants.EN_SETTINGS:
        missing = common.get_missing(row, total)
        full_row = list(row) + missing
        full_row[6] = language
        settings_rows.append(full_row)
    return settings_rows


def get_page_text(formset_list):
    text_list = []
    for element in formset_list:
        if not element.field_type == 'content':
            break
        text_partial = ''.join(element.text.splitlines())
        text_list.append(text_partial)
    return ''.join(text_list)


def get_page_row(page, total, formset_list):
    page_row = [
        'G',
        '',
        page['title'],
        1,
        get_page_text(formset_list),
        '',
        'en',
    ]
    return page_row + common.get_missing(page_row, total)


ROW_FILTERS = {
    'content': content.prepare_content_row,
    'radio': radio.prepare_radio_row,
    'textarea': textarea.prepare_textarea_row,
    'select': select.prepare_select_row,
    'checkbox': checkbox.prepare_checkbox_row,
    'tabletable': tabletable.prepare_tabletable_row,
    'matrixtable': matrixtable.prepare_matrixtable_row,
    'inputtext': inputtext.prepare_inputtext_row,
}


def prepare_formset_list(formset_list, total):
    prepared_formset_list = []
    for formset in formset_list:
        if formset.field_type in ROW_FILTERS:
            prepare_callable = ROW_FILTERS[formset.field_type]
            partial_formset_list = prepare_callable(formset, total)
            prepared_formset_list += partial_formset_list
        else:
            assert False, "Missing row handler for: `%s`" % formset.field_type
    return prepared_formset_list


def update_language(survey_list, language):
    """Updates the language colum in the given survey_list."""
    updated_list = []
    # Column 6 contains the language definition:
    for item in survey_list:
        item[6] = language
        updated_list.append(item)
    return updated_list


def prepare_survey_list(survey_list, total, language='en'):
    prepared_survey_list = []
    for i, (page, formset_list) in enumerate(survey_list):
        page_row = get_page_row(page, total, formset_list)
        partial_list = prepare_formset_list(formset_list, total)
        if partial_list:
            prepared_survey_list.append(page_row)
            prepared_survey_list += partial_list
        else:
            logger.warning('Ignoring section because of missing fields: `%s`',
                           page)
    # Update language for the survey_list
    prepared_survey_list = update_language(prepared_survey_list, language)
    return prepared_survey_list


def convert_survey_list(survey_list, language):
    """Transform the survey elements into a list of LimeSurvey rows.

    Returns:
    - `full_list`: Tuples ready compatible with limesurvey import file.
       Contains all the required fields.
    - `questions`: Questions contained on the survey list.
    """
    # TODO: Determine dynamically name and details of the imported survey.
    total = len(constants.COLUMNS)
    row_list = [constants.COLUMNS]
    row_list += get_settings_rows(total)
    row_list += get_local_settings_rows(total, language)
    survey_list = prepare_survey_list(survey_list, total, language)
    row_list += survey_list
    updated_row_list = postprocessor.update_row_list(row_list)
    return {
        'full_list': updated_row_list,
        'questions': survey_list,
    }
