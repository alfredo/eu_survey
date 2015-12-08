import logging

from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)


"""
'Q', ';', 'afAMF', '1', '[:] Multi-Flex 1-10', '', 'en', '', '', 'N', '', '1', '', '', '', 'afSrcFilter', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '', '', '', '', '', '', '', 'maxSelect', '', '', '', '', '', 'minSelect', '', '', '', '', 'ceil(num2)', 'floor(num)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""

def get_question_row(formset, total):
    field_name = common.get_matrix_value(formset.matrix_id)
    partial_question = [
        'Q',
        ';',
        field_name,
        1,
        formset.question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
        '',
    ]
    full_question = partial_question + common.get_missing(partial_question, total)
    custom_fields = (
        ('same_default', 1),
    )
    full_question = common.update_row(full_question, custom_fields)
    return full_question

"""
'SQ', '0', 'sq1', '', 'First sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_subquestion_id(question_list):
    question_ids = set()
    for question in question_list:
        # question name: answer6251697|1|1
        q_id = 'sq%s' % question['input']['name'].split('|')[1]
        question_ids.add(q_id)
    # Subquestion id should be consistent
    if len(question_ids) == 1:
        return list(question_ids)[0]
    raise ValueError('Inconsistent subquestion naming: `%s`' % question_list)


def get_subquestion_rows(formset, total):
    subquestion_rows = []
    for name, question_list in formset.field_list:
        subquestion_id = get_subquestion_id(question_list)
        partial_row = [
            'SQ',
            0,
            subquestion_id,
            '',
            name,
            '',
            'en',
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        subquestion_rows.append(full_row)
    return subquestion_rows


def get_answers(question_list):
    question_set = set()
    for question in question_list:
        # question name: answer6251697|1|1
        name = question['input']['name'].split('|')[2]
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

"""
'SQ', '1', '1', '1', 'Never', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_answer_rows(formset, total):
    answer_set = get_answers_set(formset)
    answer_rows = []
    for name, label in answer_set:
        partial_row = [
            'SQ',
            1,
            name,
            name,
            label,
            '',
            'en',
            ''
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        answer_rows.append(full_row)
    return answer_rows


def prepare_tabletable_row(formset, total):
    tabletable_row = [get_question_row(formset, total)]
    tabletable_row += get_subquestion_rows(formset, total)
    tabletable_row += get_answer_rows(formset, total)
    return tabletable_row
