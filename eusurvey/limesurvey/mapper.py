import os
import logging

from collections import namedtuple
from eusurvey import database, query

logger = logging.getLogger(__name__)

RELEVANT_ROWS = [0, 1, 2, 4]


def create_mapper(survey_list):
    mapper_list = [
        ['class', 'type/scale', 'name', 'translation', 'text']
    ]
    for survey in survey_list:
        row = [survey[n] for n in RELEVANT_ROWS]
        # Remove text for page rows:
        if row[0] in ['G']:
            row[-1] = ''
        # Placeholder for the value translation:
        row.insert(3, '')
        mapper_list.append(row)
    logger.debug('Mapped rows: %s', len(mapper_list))
    return mapper_list


def split_map_questions(survey_map_list):
    """Splits the survey in questions."""
    survey_questions = []
    question_list = []
    total_rows = len(survey_map_list)
    for i, row in enumerate(survey_map_list):
        row_class, row_type, row_name, row_translation, text = row
        # Sections are not relevant:
        if row_class in ['G']:
            continue
        if row_class in ['Q']:
            if question_list:
                # Record the previous question
                survey_questions.append(question_list)
            question_list = [row]
        else:
            question_list.append(row)
        # Last row, record:
        if i == (total_rows - 1):
            survey_questions.append(question_list)
    return survey_questions


Translation = namedtuple('Translation', ['tool_key', 'data_key', 'values'])


def get_header_translation(question, values=None):
    """Translates the header with optional values."""
    row_class, row_type, tool_key, data_key, text = question
    values = values if values else None
    return Translation(**{
        'tool_key': tool_key,
        'data_key': data_key,
        'values': values,
    })


def get_choice_translation(question):
    """Translates a question where the values are a single choice."""
    values = {}
    for answer in question[1:]:
        if answer[0].strip() in ['A']:
            if answer[3]:
                values[answer[3]] = answer[2]
    return [get_header_translation(question[0], values)]


def get_text_translation(question):
    """Translates a text question."""
    return [get_header_translation(question[0])]


def get_radio_translation(question):
    return get_choice_translation(question)


def get_select_translation(question):
    return get_choice_translation(question)


def get_multiple_translation(question):
    # a6251625[v1626]
    question_tool_key, question_data_key = question[0][2:4]
    translation_list = []
    PATTERN = '%s[%s]'
    for answer in question[1:]:
        answer_tool_key, answer_data_key = answer[2:4]
        tool_key = PATTERN % (question_tool_key, answer_tool_key)
        if question_data_key and answer_data_key:
            data_key = PATTERN % (question_data_key, answer_data_key)
        else:
            data_key = ''
        translation_list.append(Translation(**{
            'tool_key': tool_key,
            'data_key': data_key,
            'values': None,
        }))
    return translation_list


def get_tabletable_translation(question):
    # m2016[sq2_5]
    question_tool_key, question_data_key = question[0][2:4]
    subquestion_list = []
    for subquestion in filter(lambda sq: sq[1] == '0', question[1:]):
        subquestion_list.append(subquestion[2:4])
    translation_list = []
    PATTERN = '%s[%s_%s]'
    # Loop in this order (subquestion then answer) because that's how
    # LimeSurvey does its exports and we want our answer files to be in the
    # same column order
    for subquestion_tool_key, subquestion_data_key in subquestion_list:
        for answer in filter(lambda sq: sq[1] == '1', question[1:]):
            answer_tool_key, answer_data_key = answer[2:4]
            tool_key = PATTERN % (
                question_tool_key, subquestion_tool_key, answer_tool_key)
            if all([question_data_key, subquestion_data_key, answer_data_key]):
                data_key = PATTERN % (
                    question_data_key, subquestion_data_key, answer_data_key)
            else:
                data_key = ''
            translation_list.append(Translation(**{
                'tool_key': tool_key,
                'data_key': data_key,
                'values': None,
            }))
    return translation_list


def get_tablematrix_translation(question):
    # m1707[a6251713] = v1712
    question_tool_key, question_data_key = question[0][2:4]
    answer_list = []
    for answer in filter(lambda sq: sq[0] == 'A', question[1:]):
        # Only consider translated values:
        if answer[3]:
            answer_list.append((answer[3], answer[2]))
    translation_list = []
    PATTERN = '%s[%s]'
    for subquestion in filter(lambda sq: sq[0] == 'SQ', question[1:]):
        sq_tool_key, sq_data_key = subquestion[2:4]
        tool_key = PATTERN % (question_tool_key, sq_tool_key)
        if question_data_key and sq_data_key:
            data_key = PATTERN % (question_data_key, sq_data_key)
        else:
            data_key = ''
        translation_list.append(Translation(**{
            'tool_key': tool_key,
            'data_key': data_key,
            'values': dict(answer_list),
        }))
    return translation_list


TRANSLATION_MAP = {
    'T': get_text_translation,
    'L': get_radio_translation,
    '!': get_select_translation,
    'M': get_multiple_translation,
    ';': get_tabletable_translation,
    'F': get_tablematrix_translation,
}


def get_survey_translation(survey_map_list):
    map_questions = split_map_questions(survey_map_list)
    survey_translation = []
    for question in map_questions:
        q_type = question[0][1].strip()
        if q_type in TRANSLATION_MAP:
            question_translation = TRANSLATION_MAP[q_type](question)
            survey_translation += question_translation
        else:
            logger.error('Unhandled question: %s', question[0])
    return survey_translation


def get_translated_map(survey_map_list, untranslated_headers):
    survey_map_list = list(survey_map_list)[1:]
    survey_translation = get_survey_translation(survey_map_list)
    # Generate header
    translated_map = []
    missing_translation = []
    for q_trans in survey_translation:
        if not q_trans.data_key:
            missing_translation.append(q_trans)
            logger.warning('Missing translation: `%s`', q_trans.tool_key)
        if q_trans.data_key in untranslated_headers:
            index = untranslated_headers.index(q_trans.data_key)
        else:
            index = None
        translated_map.append((index, q_trans))
    logger.info('Total columns: `%s`', len(translated_map))
    logger.info('Missing translation : `%s`', len(missing_translation))
    return translated_map


def translate_row(row, translated_map, data_index):
    translated_row = []
    for index, translation in translated_map:
        value = row[index] if index else ''
        if value and (translation.values is not None):
            # Value has a translation, replace:
            if value in translation.values:
                value = translation.values[value]
            else:
                logger.error('Dropping non-translated value: `%s`', value)
                value = ''
        translated_row.append(value)
    full_row = row[:data_index] + translated_row
    return full_row


def get_data_index(untranslated_header):
    """Determines the index for the data that should be translated.

    Assumes limesurvey fields are in this order."""
    # Ordered list of fields of limesurvey export.
    FIELDS = [
        'id',
        'submitdate',
        'lastpage',
        'startlanguage',
        'startdate',
        'datestamp',
    ]
    index = 0
    for key in FIELDS:
        try:
            index = untranslated_header.index(key)
        except ValueError:
            break
    return index + 1


def get_translated_header(untranslated_header, translated_map, data_index):
    """Determines the headers for the index."""
    header = []
    for index, translation in translated_map:
        header.append(translation.tool_key)
    full_header = untranslated_header[:data_index] + header
    return full_header


def process(url, name):
    """Main process to translate the given URL."""
    survey_dict = query.get_survey_dict(url)
    map_path = os.path.join(survey_dict['survey_path'], 'limesurvey_map.csv')
    survey_map = database.read_csv_file(map_path)
    untranslated_path = os.path.join(survey_dict['survey_path'], name)
    untranslated_rows = database.read_csv_file(untranslated_path)
    untranslated_list = list(untranslated_rows)
    untranslated_header = untranslated_list[0]
    # Determine index when the submission data starts:
    data_index = get_data_index(untranslated_header)
    translated_map = get_translated_map(survey_map, untranslated_header)
    # Prepare the translated output
    translated_header = get_translated_header(
        untranslated_header, translated_map, data_index)
    translation_list = [translated_header]
    for row in filter(None, untranslated_list[1:]):
        translated_row = translate_row(row, translated_map, data_index)
        assert len(translated_header) == len(translated_row), 'Missmatch row count'
        translation_list.append(translated_row)
    logger.info('Translated: %s', len(translation_list) - 1)
    translated_path = os.path.join(survey_dict['survey_path'], 'translated.csv')
    database.save_csv_file(translated_path, translation_list)
    return True
