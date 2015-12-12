import logging

from eusurvey import database

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


def render_content(formset):
    return [formset.text, '\n']


RENDER_MAP = {
    'tabletable': render_tabletable,
    'matrixtable': render_tabletable,
    'content': render_content,
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
        # mapped content:
        if formset.field_type in RENDER_MAP:
            render_callable = RENDER_MAP[formset.field_type]
            output += render_callable(formset)
            # link dependencies
            deps = get_dependency(formset)
            if deps:
                output.append(deps)
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
    result = result.encode('utf8')
    output_file = database.save_file(result, 'form-preview.md')
    logger.info('Output saved: `%s`', output_file)
    return result
