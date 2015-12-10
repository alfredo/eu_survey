import logging

from functools import partial
from eusurvey.limesurvey import common, constants

logger = logging.getLogger(__name__)

SIZE = len(constants.COLUMNS)


def clean_rows(row_list):
    """Returns the given rows to their original size."""
    updated_row_list = []
    for row in row_list:
        updated_row_list.append(row[:SIZE])
    return updated_row_list


def has_metadata(row):
    return len(row) > SIZE


def get_field_condition(field_id, row_list=None):
    """Returns the index of the row with the field_id searched.

    Because the columns are not ordered the list must be iterated until found.
    """
    QUESTION_TYPES = ['Q']
    SUBQUESTION_TYPES = ['SQ']
    MULTIPLE_ANSWER = ['M']
    question = None
    subquestion = None
    for i, row in enumerate(row_list):
        if row[0] in QUESTION_TYPES:
            # Document last question
            question = row
            # Reset subquestion
            subquestion = None
        if row[0] in SUBQUESTION_TYPES:
            subquestion = row
        if has_metadata(row):
            metadata = row[-1]
            if isinstance(metadata['field_id'], list):
                question_name = common.get_row_value(question, 'name')
                subquestion_name = common.get_row_value(subquestion, 'name')
                row_value = common.get_row_value(row, 'name')
                return "%s_%s == '%s'" % (
                    question_name, subquestion_name,  row_value)
            if field_id == metadata['field_id']:
                question_name = common.get_row_value(question, 'name')
                row_value = common.get_row_value(row, 'name')
                if question[1] in MULTIPLE_ANSWER:
                    return "%s_%s == 'Y'" % (question_name, row_value)
                return "%s == '%s'" % (question_name, row_value)
    logger.error('Missing triggers for: `%s`', field_id)
    return None


def add_dependencies(row_list):
    get_condition = partial(get_field_condition, row_list=row_list)
    for i, row in enumerate(row_list):
        if has_metadata(row):
            metadata = row[-1]
            if 'triggers' in metadata and metadata['triggers']:
                conditions = set([get_condition(t) for t in metadata['triggers']])
                conditions = filter(None, conditions)
                if conditions:
                    conditions = sorted(conditions)
                    common.update_row(row, (
                        ('relevance', ' OR '.join(conditions)),
                    ))
    return row_list


POSTPROCESS_FILTERS = (
    add_dependencies,
)


def update_row_list(row_list):
    for postprocess_callable in POSTPROCESS_FILTERS:
        row_list = postprocess_callable(row_list)
    # Removes any metadata appended in the rows
    return clean_rows(row_list)
