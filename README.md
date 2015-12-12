# EUSurvey bridge

This tool gathers and maps EUSurvey fields into a LimeSurvey format.


## Installation

To install grab a copy of the repository.

Install the requirements:

    pip install -r requirements.txt


And install the python package with:

    python setup develop


## Import a survey

The command to import a survey is:

    survey.py --ingest URL

Where `URL` is a EUSurvey URL. e.g.

    survey.py --ingest https://ec.europa.eu/eusurvey/runner/Platforms/


# Submit exported answers to a survey

Once the survey answers are ready to be sent back to the EUSurvey service they must be exported with:

- A CSV file format.
- Headings using the "question code".
- Using "answer codes" without converting the `Y` and `N` values.

After this data has been exported it must be placed inside the `db` directory of the survey, and must be named `answers-export.csv`.

After this is completed the form is ready to be sent to the service with the following command:

    survey.py --forward URL

Where `URL` is a EUSurvey URL. e.g.

    survey.py --forward https://ec.europa.eu/eusurvey/runner/Platforms/

This command will send back the survey exports one by one. Please note that the tool will stop if a row is not ready to be sent.


