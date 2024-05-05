#!/bin/bash

virtualenv --python=/usr/local/bin/python3.7 venvAPI
source ./venvAPI/bin/activate && pip install pytest==3.10.1 requests urllib3 configparser pytest-html && pytest -v test_cases_for_location_api.py --junitxml=./reports/execution_report.xml
