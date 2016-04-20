import logging

from eusurvey.fields.common import to_str

logger = logging.getLogger(__name__)


def prepare_content_row(formset, total):
    """Extracts content rows.

    IMPORTANT: ection headers are handled in `fields.importer.get_form_page`
    because of that this type of content is ignored."""
    return []
