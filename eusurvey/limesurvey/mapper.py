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
    for row in survey_map_list:
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
    return survey_questions


Translation = namedtuple('Translation', ['tool_key', 'data_key', 'values'])


def get_header_translation(question, values=None):
    """Translates the header with optional values."""
    row_class, row_type, tool_key, data_key, text = question
    values = values if values else []
    return Translation(**{
        'tool_key': tool_key,
        'data_key': data_key,
        'values': values,
    })


def get_text_translation(question):
    """Translates a text question."""
    return [get_header_translation(question[0])]


def get_radio_translation(question):
    """Translates a radio question."""
    values = {}
    for answer in question[1:]:
        if answer[0].strip() in ['A']:
            if answer[3]:
                values[answer[3]] = answer[2]
    return [get_header_translation(question[0], values)]


TRANSLATION_MAP = {
    'T': get_text_translation,
    'L': get_radio_translation,
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


def translate_row(row, translated_map):
    translated_row = []
    for index, translation in translated_map:
        value = row[index] if index else ''
        if translation.values:
            # Translation found for the value. Replace:
            if value in translation.values:
                value = translation.values[value]
            else:
                # TODO: Improve logging
                # Non translated values can't be accepted. Dropping:
                logger.error('Dropping non-translated value: `%s`', value)
                value = ''
        translated_row.append(value)
    full_row = row[:6] + translated_row
    return full_row


def get_translated_header(untranslated_header, translated_map):
    header = []
    for index, translation in translated_map:
        header.append(translation.tool_key)
    full_header = untranslated_header[:6] + header
    return full_header


def process(url, name):
    survey_dict = query.get_survey_dict(url)
    map_path = os.path.join(survey_dict['survey_path'], 'limesurvey_map.csv')
    survey_map = database.read_csv_file(map_path)
    untranslated_path = os.path.join(survey_dict['survey_path'], name)
    untranslated_rows = database.read_csv_file(untranslated_path)
    untranslated_list = list(untranslated_rows)
    untranslated_header = untranslated_list[0]
    translated_map = get_translated_map(survey_map, untranslated_header)
    # Prepare the translated output
    translation_list = [
        get_translated_header(untranslated_header, translated_map)]
    for row in filter(None, untranslated_list[1:]):
        translated_row = translate_row(row, translated_map)
        logger.info(translated_row)
        translation_list.append(translated_row)
    logger.info('Translated: %s', len(translation_list) - 1)
