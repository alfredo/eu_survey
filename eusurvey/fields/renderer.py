import logging

logger = logging.getLogger(__name__)


def _id(field):
    if not field['input']['id']:
        return ''
    name = field['input']['id'].replace('trigger', '')
    return '<a id="%s"></a> [%s] ' % (name, name)


def render_tabletable(formset):
    output = ['## [%s] %s' % (formset.field_type.upper(), formset.question)]
    for title, field_list in formset.field_list:
        output.append('    ### %s' % title)
        for field in field_list:
            output.append(
                ' - %s %s' % (_id(field), field['label']))
    return output


def render_matrixtable(formset):
    output = ['## [%s] %s' % (formset.field_type.upper(), formset.question)]
    for title, field_list in formset.field_list:
        output.append('   ### %s' % title)
        for field in field_list:
            output.append(
                ' - %s %s' % (_id(field), field['label']))
    return output


RENDER_MAP = {
    'tabletable': render_tabletable,
    'matrixtable': render_tabletable,
}


def get_dependency(formset):
    deps = []
    if formset.is_supplementary:
        for trigger in formset.data_triggers:
            deps.append('[View %s.](#user-content-%s)' % (trigger, trigger))
    return u' '.join(deps)


def render_field_list(formset_list, start=1):
    output = []
    counter = 1
    for formset in formset_list:
        # Is it only text:
        if isinstance(formset, basestring):
            output += [formset, '\n']
            continue
        # Is it mapped:
        if formset.field_type in RENDER_MAP:
            render_callable = RENDER_MAP[formset.field_type]
            output += render_callable(formset)
            continue
        output.append('## [%s] %s. `%s`' % (
            formset.field_type.upper(), counter, formset.question))
        if formset.help_text:
            output.append(formset.help_text)
        if formset.field_list:
            for field in formset.field_list:
                output.append(
                    ' - %s %s' % (_id(field), field['label']))
        if formset.option_list:
            for option in formset.option_list:
                output.append(' - %s %s' % (_id(option), option['label']))

        counter += 1
        deps = get_dependency(formset)
        if deps:
            output.append(deps)
    return output


def render(survey_list):
    output = []
    for page, formset_list in survey_list:
        output.append('# %s' % page['title'])
        output += render_field_list(formset_list)
    result = u'\n\n'.join(output)
    logger.info(result)
    return result.encode('utf8')


# def foo():
#     for i, formset in enumerate(formset_list, start=1):
#         output.append('%s. `%s`' % (i, formset.question))
#         if formset.field_list:
#             for field in formset.field_list:
#                 output.append('    - [%s] %s' % (field['input']['id'], field['label']))
#         if formset.option_list:
#             for option in formset.option_list:
#                 output.append('    - %s' % option['text'])
#         msg = '      ^^ (Supplementary)" %s' %  formset.data_triggers if formset.is_supplementary else ''
#         if msg:
#             output.append(msg)
#     result = '\n'.join(output)
#     logger.info(result)
#     return result
