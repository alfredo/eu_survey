from eusurvey.limesurvey import common

"""Example:
['Q', 'T', 'Q03', 'Q01_NA == "Y"', 'Please describe in as much detail as possible why you do not purchase any electronics.', '', 'en', '', '', 'N', '', '1', '', '', '', '', '', '', '', '', '6', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '70', '1']
"""


def prepare_textarea_row(formset, total):
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
    return [full_row]
