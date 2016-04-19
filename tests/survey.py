from eusurvey import query


def test_cleaned_url_is_left_untouched_without_params():
    url = ('https://ec.europa.eu/eusurvey/runner/Consultation_Copyright'
           '?surveylanguage=EN')
    result = query.clean_url(url, None)
    assert result == url


def test_cleaned_url_replaces_passed_params():
    url = ('https://ec.europa.eu/eusurvey/runner/Consultation_Copyright'
           '?surveylanguage=EN')
    result = query.clean_url(url, {'surveylanguage': 'DE'})
    assert result == (
        'https://ec.europa.eu/eusurvey/runner/Consultation_Copyright'
        '?surveylanguage=DE')
