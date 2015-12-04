import logging

logger = logging.getLogger(__name__)


def render(formset_list):
    for i, formset in enumerate(formset_list, start=1):
        logger.info('%s. `%s`', i, formset.question)
        if formset.field_list:
            for field in formset.field_list:
                logger.info('    - %s', field['label'])
        if formset.field:
            msg = '^^ (Supplementary)' if formset.is_supplementary else ''
            logger.warning('%s', msg)
        if formset.option_list:
            for option in formset.option_list:
                logger.info('    - %s', option['text'])
    return True
