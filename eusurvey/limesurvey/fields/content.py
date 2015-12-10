import logging

from eusurvey.fields.common import to_str

logger = logging.getLogger(__name__)


def prepare_content_row(formset, total):
    # Ignoring content rows. Text is handled in the page heading:
    return []
