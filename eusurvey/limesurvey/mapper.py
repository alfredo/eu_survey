import logging

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
