from eusurvey import database, reader
from eusurvey.fields import importer

from eusurvey.poster import submission





URL = 'https://ec.europa.eu/eusurvey/runner/Platforms/'


def run(url=URL):
    tree = reader.get_form_tree(url)
    pre_submission = submission.prepare_submission(tree)
    # TODO: Capture user input (replace dummy_payload):
    dummy_payload = parse_qs(PAYLOAD)
    dummy_payload.update(pre_submission.payload)
    # success_result = send_submission(url, dummy_payload, pre_submission)
    # Backup response
    # database.save_output(response.content, name='%s.html' % success_response.uid)
    result = database.read_output(
        name='bf31722d-a7d2-4a16-b3c8-b0af9c34d598.html')
    assert False, result
    # print success_result
    print "Done."


def import_fields(url=URL):
    """Imports the given form fields"""
    importer.process(url)
    return True


def submit_surveys(name='results-survey.csv', url=URL):
    submission.process(name, url)
    return True
