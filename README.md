# EUSurvey bridge

This tool gathers and maps EUSurvey fields into a LimeSurvey format.


## Installation

To install grab a copy of the repository.

Install the requirements:

    pip install -r requirements.txt


And install the python package with:

    python setup develop


## Imoprt a survey

The command to import a survey is:

    survey.py --ingest URL

Where `URL` is a EUSurvey URL. e.g.

    survey.py --ingest https://ec.europa.eu/eusurvey/runner/Platforms/


