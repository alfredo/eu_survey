import logging

logger = logging.getLogger(__name__)

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
)


def get_settings_rows(total):
    settings_rows = []
    for row in constants.GLOBAL_SETTINGS:
        missing = common.get_missing(row, total)
        full_row = list(row) + missing
        settings_rows.append(full_row)
    return settings_rows


def get_local_settings_rows(total):
    settings_rows = []
    for row in constants.EN_SETTINGS:
        missing = common.get_missing(row, total)
        full_row = list(row) + missing
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


def prepare_survey_list(survey_list, total):
    prepared_survey_list = []
    for i, (page, formset_list) in enumerate(survey_list):
        prepared_survey_list.append(get_page_row(page, total, formset_list))
        # Add any hard rows:
        if i == 0:
            prepared_survey_list += constants.HARD_ROWS
        partial_list = prepare_formset_list(formset_list, total)
        if partial_list:
            prepared_survey_list += partial_list
    return prepared_survey_list


def make_limesurvey_file(survey_list):
    """Transform the survey elements into a list of LimeSurvey rows."""
    total = len(constants.COLUMNS)
    row_list = [constants.COLUMNS]
    row_list += get_settings_rows(total)
    row_list += get_local_settings_rows(total)
    row_list += prepare_survey_list(survey_list, total)
    updated_row_list = postprocessor.update_row_list(row_list)
    return updated_row_list
