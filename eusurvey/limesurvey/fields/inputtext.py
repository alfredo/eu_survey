from eusurvey.limesurvey import common


def prepare_inputtext_row(formset, total):
    field_name = common.get_name(formset.field['name'])
    partial_row = [
        'Q',
        'T',
        field_name,
        1,
        formset.question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
    ]
    full_row = partial_row + common.get_missing(partial_row, total)
    if formset.limits:
        column_definition = (
            ('maximum_chars', formset.limits[-1]),
        )
    else:
        column_definition = ()
    full_row = common.update_row(full_row, column_definition)
    # Add row metadata:
    full_row.append(formset.get_dependencies())
    return [full_row]
