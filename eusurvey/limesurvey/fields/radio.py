from eusurvey.limesurvey import common


def get_question_row(formset, total):
    field_name = common.get_name(formset.field_list[0]['input']['name'])
    partial_question = [
        'Q',
        'L',
        field_name,
        1,
        formset.question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
        '',
    ]
    full_row = partial_question + common.get_missing(partial_question, total)
    # Add metadata:
    full_row.append(formset.get_dependencies())
    return full_row


def get_answer_row(field, total):
    row_value = common.get_value(field['input']['value'])
    partial_row = [
        'A',
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
    # Add row metadata:
    metadata = {
        'field_id': field['input'].get('id'),
    }
    full_row.append(metadata)
    return full_row


def prepare_radio_row(formset, total):
    radio_row = [get_question_row(formset, total)]
    for field in formset.field_list:
        radio_row.append(get_answer_row(field, total))
    return radio_row
