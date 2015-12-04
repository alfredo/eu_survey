import logging

logger = logging.getLogger(__name__)


def render(formset_list):
    output = []
    for i, formset in enumerate(formset_list, start=1):
        output.append('%s. `%s`' % (i, formset.question))
        if formset.field_list:
            for field in formset.field_list:
                output.append('    - %s' % field['label'])
        if formset.option_list:
            for option in formset.option_list:
                output.append('    - %s' % option['text'])
        msg = '      ^^ (Supplementary)' if formset.is_supplementary else ''
        if msg:
            output.append(msg)
    result = '\n'.join(output)
    logger.info(result)
    return result
