import logging

from eusurvey import submission, models
from eusurvey.fields import validators

logger = logging.getLogger(__name__)

from lxml import etree


IGNORED_CLASS = ['surveytitle']

_str = etree.tostring


def _get(element_list, expected=1):
    """Validates there is a single element in the list."""
    if not len(element_list) == expected:
        raise ValueError(
            'Different number of elements than expected: `%s`' % element_list)
    return element_list[0]


def is_mandatory(question):
    """Determines if the question is mandatory."""
    return bool(question.xpath('.//span[@class="mandatory"]/text()'))


def get_label(field_element):
    """Determines the label for the field_element."""
    label_field = _get(field_element.xpath('.//td/label'))
    label_text = _get(
        label_field.xpath('.//span[@class="answertext"]/text()'))
    label_pk = label_field.attrib['for']
    return models.Label(text=label_text, pk=label_pk)


def get_field_list(section):
    field_element_list = section.xpath('.//table[@class="answers-table"]/tr')
    field_list = []
    for field_element in field_element_list:
        label = get_label(field_element)
        input_field = _get(field_element.xpath('.//td/input'))
        field = models.Field(label=label, widget=input_field)
        field_list.append(field)
    return field_list


def extract_formset(section):
    if not validators.is_fields_section(section):
        return None
    question_element = _get(section.xpath('.//div[@class="questiontitle"]'))
    mandatory = is_mandatory(question_element)
    question = question_element.xpath('.//td')[1].text
    field_list = get_field_list(section)
    return models.FormSet(
        question=question, is_mandatory=mandatory, field_list=field_list)


def get_form_elements(tree):
    """Extracts the fields containers."""
    return tree.xpath('//form/div/div/div')


def get_form_title(tree):
    """Gets the title of the form."""
    # <div class="surveytitle">
    return tree.xpath('//div[@class="surveytitle"]/text()')[0]


def get_form_sections(tree):
    """Extracts the forms sections from the given tree."""
    section_list = []
    for section in tree.xpath('//div[contains(@class, "pagebutton")]'):
        data_id = section.attrib['data-id']
        title = section.xpath('a/div/text()')[0].strip()
        html_id = section.xpath('a/@id')[0].strip()
        section_list.append((data_id, {
            'title': title,
            'html_id': html_id,
        }))
    return section_list


def process(url):
    tree = submission.get_form_tree(url, use_cache=True)
    title = get_form_title(tree.tree)
    sections = get_form_sections(tree.tree)
    form_elements = get_form_elements(tree.tree)
    formset_list = []
    for element in form_elements:
        # Ignore non valid elements:
        if not validators.is_valid_element(element):
            continue
        formset = extract_formset(element)
        if not formset:
            continue
        formset_list.append(formset)
    return models.Form(**{
        'title': title,
        'sections': sections,
        'formset_list': formset_list,
    })
