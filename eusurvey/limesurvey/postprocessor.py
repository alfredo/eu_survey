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


QUESTION_TYPES = ['Q']
SUBQUESTION_TYPES = ['SQ']
MULTIPLE_ANSWER = ['M']


def get_field_condition(field_id, row_list=None):
    """Condition for the field_id searched.

    Because previous rows can affect the outcome it needs to be
    iterated sequentially until found."""
    question = None
    subquestion_list = []
    for i, row in enumerate(row_list):
        # Reset relevant fields:
        question_name = None
        row_value = None
        row_type = row[0].strip()
        if row_type in QUESTION_TYPES:
            # Document last question
            question = row
            # Next subquestions are part of this question:
            subquestion_list = []
        if row_type in SUBQUESTION_TYPES:
            subquestion_list.append(common.get_row_value(row, 'name'))
        # Before skipping needs to record any question/subquestion:
        if not has_metadata(row):
            # Ignore fields without metadata:
            continue
        metadata = row[-1]
        # Handle direct fields:
        if field_id == metadata['field_id']:
            question_name = common.get_row_value(question, 'name')
            row_value = common.get_row_value(row, 'name')
            if question[1] in MULTIPLE_ANSWER:
                return "%s_%s == 'Y'" % (question_name, row_value)
            else:
                return "%s == '%s'" % (question_name, row_value)
        # Matrix fields. They are compressed into a row per subquestion/answer
        # For this reason they have multiple ids:
        q_subtype = question[1].strip()
        matrix_conditions = [
            isinstance(metadata['field_id'], list),
            q_subtype in ['F'],
            field_id in metadata['field_id'],
        ]
        if all(matrix_conditions):
            question_name = common.get_row_value(question, 'name')
            row_value = common.get_row_value(row, 'name')
            condition_list = []
            for subquestion in subquestion_list:
                condition_list.append(
                    "%s_%s == '%s'" % (question_name, subquestion,  row_value))
            conditions = ' OR '.join(sorted(condition_list))
            return conditions
    logger.error('Missing triggers for: `%s`', field_id)
    return None


CONDITION_REPLACEMENTS = {
    "a6251561 == 'v1570' OR a6251573 == 'v1574' OR a6251573 == 'v1575'":
    "a6251561 == 'v1570' OR a6251561 == 'v1567'",
    "a6497498 == 'v7507' OR a6497510 == 'v7511' OR a6497510 == 'v7512'":
    "a6497498 == 'v7507' OR a6497498 == 'v7504'",
}


def add_dependencies(row_list):
    """Adds any dependency between the given rows using the metadata."""
    get_condition = partial(get_field_condition, row_list=row_list)
    for i, row in enumerate(row_list):
        if not has_metadata(row):
            # Row has no dependencies. Ignore.
            continue
        metadata = row[-1]
        # `triggers` are the fields that activate this field:
        if 'triggers' in metadata and metadata['triggers']:
            logger.info('%s - %s', i, metadata['triggers'])
            conditions = set([get_condition(t) for t in metadata['triggers']])
            conditions = filter(None, conditions)
            if conditions:
                conditions = sorted(conditions)
                conditions_str = ' OR '.join(conditions)
                logger.debug(conditions_str)
                if conditions_str in CONDITION_REPLACEMENTS:
                    new_str = CONDITION_REPLACEMENTS[conditions_str]
                    logger.info('Replacing `%s` with `%s`', conditions_str, new_str)
                    conditions_str = new_str
                common.update_row(row, (
                    ('relevance', conditions_str),
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
