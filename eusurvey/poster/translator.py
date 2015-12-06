import re


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
    key = key.replace('a', answer_prefix)
    value = answer_prefix.replace('answer', '') + value.replace(']', '')
    # This field contains the value and the key in the column.
    # in limesurvey the value is a `Y` or `N`. So when a Y is present
    # this value should be sent.
    return (key, value)


def update_key(key, answer_prefix):
    if is_short_answer(key):
        return key.replace('a', 'answer')
    if ('[' in key) and ('_' in key):
        return get_tabletable_key(key, answer_prefix)
    if '[v' in key:
        return get_checkbox_key(key, answer_prefix)
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


def prepare_payload(row, row_map):
    payload = {}
    for key, value in zip(row_map, row):
        if key in IGNORED_KEYS:
            continue
        key = update_key(key)
        payload[key] = value
    return payload
