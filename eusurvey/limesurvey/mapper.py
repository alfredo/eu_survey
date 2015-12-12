import os
import logging

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
    logger.info('Mapped rows: %s', len(mapper_list))
    return mapper_list



def update_mapped_survey(survey_map, untranslated_rows):
    # GENERATE expected headings + add missing columns
    survey_headings = []
    for row in survey_map:
        assert False, row
    assert False, (survey_map, untranslated_rows)


def process(url, name):
    survey_dict = query.get_survey_dict(url)
    map_path = os.path.join(survey_dict['survey_path'], 'limesurvey_map.csv')
    survey_map = database.read_csv_file(map_path)
    untranslated_path = os.path.join(survey_dict['survey_path'], name)
    untranslated_rows = database.read_csv_file(untranslated_path)
    updated_rows = update_mapped_survey(survey_map, untranslated_rows)
    assert False, updated_rows
