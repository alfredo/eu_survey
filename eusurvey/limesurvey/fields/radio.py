from eusurvey.limesurvey import common


def prepare_radio_row(formset, total):
    field_name = common.get_name(formset.field_list[0]['input']['name'])
    partial_question = [
        'Q',
        'L',
        field_name,
        1,
        formset.question,
        '',
        'en',
        '',
        'Y' if formset.is_mandatory else '',
        '' # Other: link to please specfy?
    ]
    question_row = partial_question + common.get_missing(partial_question, total)
    radio_row = [question_row]
    for i, field in enumerate(formset.field_list):
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
            '' # Other: link to please specfy?
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        radio_row.append(full_row)
    return radio_row
