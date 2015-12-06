import re

from collections import defaultdict


def is_short_answer(key):
    return re.match(r'^a([\d]+)$', key)


def get_tabletable_key(original_key, answer_prefix):
    raw_key, raw_answers = original_key.split('[')
    key = raw_key.replace('m', answer_prefix)
    sub_question, value = raw_answers.replace(']', '').split('_')
    key += '|%s|%s' % (sub_question.replace('sq', ''), value)
    return key


def get_checkbox_key(original_key, answer_prefix):
    key, value = original_key.split('[v')
    key = key.replace('a', 'answer')
    value = answer_prefix.replace('answer', '') + value.replace(']', '')
    # This field contains the value and the key in the column.
    # in limesurvey the value is a `Y` or `N`. So when a Y is present
    # this value should be sent.
    return (key, value)


def get_matrixtable_key(original_key, answer_prefix):
    matrix, key = original_key.split('[')
    return key.replace(']', '').replace('a', 'answer')


def update_key(key, answer_prefix):
    if is_short_answer(key):
        return key.replace('a', 'answer')
    if ('[' in key) and ('_' in key):
        return get_tabletable_key(key, answer_prefix)
    if '[v' in key:
        return get_checkbox_key(key, answer_prefix)
    if key.startswith('m') and '[a' in key:
        return get_matrixtable_key(key, answer_prefix)
    return key


def get_answer_prefix(key_map):
    for key in key_map:
        if is_short_answer(key):
            return key[:4].replace('a', 'answer')
    raise ValueError('Could not find the answer prefix.')


def update_key_map(key_map):
    k_list = []
    answer_prefix = get_answer_prefix(key_map)
    for key in key_map:
        k_list.append(update_key(key, answer_prefix))
    return k_list


IGNORED_KEYS = [
    'submitdate',
    'lastpage',
    'startlanguage',
    'startdate',
    'datestamp',
]


def is_short_value(value):
    return re.match(r'^v([\d]+)$', value)


def update_value(value, value_prefix):
    if is_short_value(value):
        return value.replace('v', value_prefix)
    return value


def get_value_prefix(row_map):
    for row in row_map:
        if row.startswith('answer'):
            return row[6:9]
    raise ValueError('Could not find the value prefix.')


def prepare_payload(row, row_map):
    payload = defaultdict(list)
    value_prefix = get_value_prefix(row_map)
    for key, value in zip(row_map, row):
        if key in IGNORED_KEYS:
            continue
        if isinstance(key, tuple):
            key, translated_value = key
            value = translated_value if value.lower() == 'y' else ''
        payload[key].append(update_value(value, value_prefix))
    return payload
