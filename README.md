**QA Automation Project**

**Description**

This project is related with the integration between the endpoints and the front end of the application.

The BE section focus on test endpoints provided for an application (GET, POST, DELETE, PUT), this type of automation
covers the integration of the endpoints and the Front end, this testing validates if BE and FE together behave as expected.

**Technologies Used**

The BE project use the following python packages:

    - Python 3.10.7
    - pytest
    - requests
    - urllib3
    - configparser
    - pytest-html


**How to execute automation projects**

**BE project execution steps**

In order to execute the BE project, the following steps are required:

1. Installation of the required packages previously mentioned

2. Type the following command in terminal:

        cd  ~/path-where-project-lives/api_project_demo

3. in the terminal type:

    a. if a report is required use this command:

            pytest -v test_cases_for_location_api.py --html=./reports/execution_report.html


    a1. in order to check the report, run this open the html file created inside reports folder

    b. if report is not required use this command:

            pytest -v test_cases_for_location_api.py

4. Wait until the execution of the project finishes.

