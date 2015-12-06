import logging

from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)

"""
'SQ', '0', 'sq2', '', 'Second sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'SQ', '0', 'sq3', '', 'Third sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'SQ', '0', 'sq4', '', 'Fourth sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'SQ', '0', 'sq5', '', 'Fifth sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''

'A', '0', '2', '2', 'Medium', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'A', '0', '3', '3', 'High', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""

"""
'Q', 'F', 'afAFR', '1', '[F] Flexible Array (Row)', '', 'en', '', '', 'N', '', '1', '', '', '', 'afSrcFilter', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'maxSelect', '', '', '', '', '', 'minSelect', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""

def get_question_row(formset, total):
    field_name = common.get_matrix_value(formset.matrix_id)
    partial_question = [
        'Q',
        'F ',
        field_name,
        1,
        formset.question,
        '',
        'en',
        '',
        common.get_mandatory(formset),
        '' # Other: link to please specfy?
    ]
    full_question = partial_question + common.get_missing(partial_question, total)
    return full_question

"""
'A', '0', '1', '1', 'Low', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_answers(question_list):
    question_set = set()
    for question in question_list:
        name = common.get_value(question['input']['value'])
        question_set.add((name, question['label']))
    return question_set


def get_answers_set(formset):
    answer_set = set()
    total_answers = 0
    for name, question_list in formset.field_list:
        answers = get_answers(question_list)
        total_answers = len(answers)
        answer_set.update(answers)
    assert len(answer_set) == total_answers, "Invalid answer count. `%s`" % formset
    return answer_set


def get_answer_rows(formset, total):
    answer_set = get_answers_set(formset)
    answer_rows = []
    for name, label in answer_set:
        partial_row = [
            'A',
            0,
            name,
            name,
            label,
            '',
            'en',
            '',
            '',
            '' # Other: link to please specfy?
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        answer_rows.append(full_row)
    return answer_rows


"""
'SQ', '0', 'sq1', '', 'First sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_subquestion_id(question_list):
    question_ids = set()
    for question in question_list:
        question_ids.add(question['input']['name'])
    if len(question_ids) == 1:
        return list(question_ids)[0]
    raise ValueError('Inconsistent subquestion naming: `%s`' % question_list)


def get_subquestion_rows(formset, total):
    subquestion_rows = []
    for name, question_list in formset.field_list:
        subquestion_id = get_subquestion_id(question_list)
        field_name = common.get_name(subquestion_id)
        partial_row = [
            'SQ',
            0,
            field_name,
            '',
            name,
            '',
            'en',
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        subquestion_rows.append(full_row)
    return subquestion_rows


def prepare_matrixtable_row(formset, total):
    matrixtable_row = [get_question_row(formset, total)]
    matrixtable_row += get_subquestion_rows(formset, total)
    matrixtable_row += get_answer_rows(formset, total)
    return matrixtable_row
