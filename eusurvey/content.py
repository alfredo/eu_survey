from eusurvey.fields.common import to_str, get


PATTERN_LIST = [
    u'.//div[contains(@class, "sectiontitle")]',
    u'.//div[@class="text"]',
]


def extractor(section):
    for pattern in PATTERN_LIST:
        result = section.xpath(pattern)
        if result:
            return unicode(get(section.xpath(pattern)).text_content())
    return None
