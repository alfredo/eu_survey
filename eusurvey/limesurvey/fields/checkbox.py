import logging

from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)


"""
'Q', 'M', 'Q01', '1', 'Which of the following electronics have you purchased in the last 6 months?', '', 'en', '', '', 'Y', '', '1', '', '', '', '', '', '', '', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'NA', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Other electronic', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'SQ', '0', 'A', '', ' Product A', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'SQ', '0', 'B', '', ' Product B', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""

def get_question_row(formset, total):
    question_name = formset.field_list[0]['input']['name']
    field_name = common.get_name(question_name)
    question = ' '.join(formset.question.splitlines())
    partial_question = [
        'Q',
        'M',
        field_name,
        1,
        question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
        '',
    ]
    full_row = partial_question + common.get_missing(partial_question, total)
    # TODO: find out a way to express the limit as words too:
    if formset.limits and len(formset.limits) == 2:
        min_a, max_a = formset.limits
        column_definition = (
            ('min_answers', min_a),
            ('max_answers', max_a),
        )
        full_row = common.update_row(full_row, column_definition)
    full_row.append(formset.get_dependencies())
    return full_row


"""
{'input': {'name': 'answer6251625', 'value': '6251626', 'data-dependencies': [''], 'data-id': '62516256251626', 'type': 'checkbox', 'id': '6251626'}, 'label': 'make information more accessible'}
"""


def get_answer_row(field, total):
    # Multiple select fields use the same field name to send
    # different values. Unfortunately lime survey doesn't support
    # this type of format. Checkboxes fields are represented as a
    # list of fields with different names and a `Y` value  is sent
    # when the field is checked.
    # Since the `id` and `value` field name are the same a
    # workaround is to send a special `value` that will be reversed
    # as the field ID to extract the original `name` and the value
    # can be attached . e.g
    #   value='6251626' compressed to `v1626`
    #   `v1626` references field ID `6251626` and the field contains
    #   `name` and `value` to be sent back.
    row_value = common.get_value(field['input']['value'])
    partial_row = [
        'SQ',
        0,
        row_value,
        '',
        field['label'],
        '',
        'en',
        '',
        '',
        '',
    ]
    full_row = partial_row + common.get_missing(partial_row, total)
    metadata = {
        'field_id': field['input'].get('id'),
    }
    full_row.append(metadata)
    return full_row


def prepare_checkbox_row(formset, total):
    checkbox_row = [get_question_row(formset, total)]
    for field in formset.field_list:
        checkbox_row.append(get_answer_row(field, total))
    return checkbox_row
