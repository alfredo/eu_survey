import logging

from eusurvey.fields.common import to_str
from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)

"""
['Q', 'X', 'a7738563', '1', 'AAAAAA', '', 'en', '', '', 'N', '', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
"""


def get_text_row(formset, total):
    field_name = u'a%s' % formset.field['id']
    partial_row = [
        'Q',
        'X',
        field_name,
        1,
        formset.field['text'],    # Text content
        '',                       # Help text
        'en',
        '',
        '',
    ]
    full_row = partial_row + common.get_missing(partial_row, total)
    common.update_row(full_row, (
        ('other', 'N'),
        ('same_default', '1'),
        ('statistics_showgraph', '1'),
        ('time_limit_action', '1'),
    ))
    # Add row metadata:
    # full_row.append(formset.get_dependencies())
    return [full_row]


def prepare_content_row(formset, total):
    """Extracts content rows.

    IMPORTANT: ection headers are handled in `fields.importer.get_form_page`
    because of that this type of content is ignored."""
    if formset.is_text():
        return get_text_row(formset, total)
    return []
