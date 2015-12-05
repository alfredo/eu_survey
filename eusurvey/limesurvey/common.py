def get_missing(row, total):
    row_count = len(row)
    missing = total - row_count
    return [''] * missing


def get_name(name):
    # Shortens the name of the answer by removing the prefix
    return name.replace('answer', 'a')


def get_value(value):
    # Removes the first 4 chars that can be pick from the answer name:
    return value[4:]


def get_mandatory(formset):
    return 'Y' if formset.is_mandatory else ''
