from eusurvey.fields.common import to_str, get, get_inner_html


PATTERN_LIST = [
    u'.//div[contains(@class, "sectiontitle")]',
    u'.//div[@class="text"]',
]


class Content:
    text = ''
    field_type = 'content'
    is_supplementary = False

    def __init__(self, section):
        self.section = section

    def is_content(self):
        for pattern in PATTERN_LIST:
            result = self.section.xpath(pattern)
            if result:
                self.text = self.extract_content(result)
                return True
        return False

    def extract_content(self, result):
        content = get(result)
        return to_str(content)


def extractor(section):
    content = Content(section)
    if content.is_content():
        return content
    return None
