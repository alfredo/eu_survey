def get_missing(row, total):
    row_count = len(row)
    missing = total - row_count
    return [''] * missing


def get_name(name):
    """Shortens the name of the answer by removing the prefix"""
    return name.replace('answer', 'a')


def get_value(value):
    """Returns a unique number for the value.

    All values have consecutive numbers e.g.

    `6251626` can be represented by `1626`.

    By using this notation it allows up to `9999` fields to be used
    in the form."""
    return value[3:]


def get_mandatory(formset):
    """Generates the mandatory field representation for LimeSurvey."""
    return 'Y' if formset.is_mandatory else ''
