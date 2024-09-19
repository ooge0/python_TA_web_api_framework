<!-- Header Section -->
<p align="left">
  <img alt="python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" width="80"/>
  <img alt="pytest" src="https://img.shields.io/badge/py-test-blue?logo=pytest" width="80"/>
  <img alt="selenium" src="https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white" width="90"/>
  <img alt="requests" src="https://img.shields.io/badge/-requests-%43B02A?style=for-the-badge&logo=requests&logoColor=white" width="75"/>
  <img alt="PyCharm" src="https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green" width="90"/>
  <img alt="pylint" src="https://raw.githubusercontent.com/pylint-dev/pylint/main/doc/logo.png" width="28"/>
</p>
<p>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge" width="100"/>
</p>


**_Test automation framework for testing UI, front-end and  back-end API of restful-booker web site - https://automationintesting.online_.**

# Table of contents <div id="toc"></div>
1. [Resources of web app](#resources-of-web-app)
   1. [Restful-booker app resources](#restful-booker-app-resources)
      1. [Restful-booker web site URL](#restful-booker-web-site-url)
      2. [Restful-booker API](#restful-booker-api)
   2. [Booking side](#booking-side)
      1. [Home web page](#home-web-page)
         1. [Basic structure of Home web page](#basic-structure-of-home-web-page)
      2. [Booking web page](#booking-web-page)
   3. [Admin Side](#admin-side)
      1. [Admin (Rooms) Web Page](#admin-rooms-web-page)
      2. [Report web page](#report-web-page)
      3. [Branding web page](#branding-web-page)
      4. [Messages web page](#messages-web-page)
2. [Test framework configuration and setup](#test-framework-configuration-and-setup)
   1. [Required python packages](#required-python-packages)
      1. [For tests itself](#for-tests-itself)
      2. [For UI/Web testing](#for-uiweb-testing)
      3. [Utils/configs](#utilsconfigs)
      4. [Logging/reporting](#loggingreporting)
      5. [Data generators](#data-generators)
      6. [DB](#db)
      7. [Assertions](#assertions)
      8. [Code analysing](#code-analysing)
3. [Project setup process](#project-setup-process)
   0. [Setup by scripts](#0setup-by-scripts) 
   1. [Create and activate a new virtual environment](#1-create-and-activate-a-new-virtual-environment)
   2. [Install required packages from requirements.txt](#2-install-required-packages-from-requirementstxt)
   3. [Check prerequisites for Allure test report generation](#3-check-prerequisites-for-allure-test-report-generation)
   4. [Usage DB as source of test data](#4-usage-db-as-source-of-test-data)
      1.  [Update DB content](#1-update-db-content)
   5. [Checking project dependency tree](#checking-project-dependency-tree)
      1. [pipdeptree](#pipdeptree)
4. [Tests](#tests) 
   1.  [Test execution by _pytest_](#test-execution-by-_pytest_)
      1. [Run all Tests](#run-all-tests)
      2. [Run tests in a module](#run-tests-in-a-module)
      3. [Test run for specific test (by test name) by command](#test-run-for-specific-test-by-test-name-by-command)
      4. [ Run Tests in a directory](#run-tests-in-a-directory)
      6. [Run tests of a specific class](#run-tests-of-a-specific-class)
      7. [Run tests by marker expressions](#run-tests-by-marker-expressions)
      5. [Run tests by node IDs](#run-tests-by-node-ids)
      8. [Additonal parts for test run/configuration](#additional-parts-for-test-runconfiguration)
         1. [Specifying configuration file location](#specifying-configuration-file-location)
         2. [Rerun failed tests](#rerun-failed-tests)
         3. [Run tests in parallel(using workers)](#run-tests-in-parallelusing-workers)
         4. [Snippets for running existing tests](#snippets-for-running-existing-tests)
      9. [Test report generation](#test-report-generation)
         1. [By pytest (Simple Report)](#by-pytest-simple-report)
         2. [By pytest (HTML Report)](#by-pytest-html-report)
         3. [By pytest (JUnit XML Report)](#by-pytest-junit-xml-report)
         4. [Test reports by Allure](#test-reports-by-allure)
            1. [Creating initial pytest reports by Allure](#creating-initial-pytest-reports-by-allure-)
   2. [Existing(created) tests by categories](#existingcreated-tests-by-categories)
      1. [Test List](#test-list)
5. [Resources for TA frameworks](#resources-for-ta-frameworks)


# Resources of web app
## Restful-booker app resources

### Restful-booker web site URL
https://automationintesting.online/
#### Restful-booker API
https://restful-booker.herokuapp.com/apidoc/index.html

## Booking side

[go to TOC](#table-of-contents)

### Home web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Home web page: https://automationintesting.online](https://automationintesting.online/)

<img src="project_related_data\pic\restful-booker_site__home_page_main.png" alt="restful-booker_site__home_page_main.png" style="width:60%;">

#### Basic structure of home web page

    ```
        logo(picture)
            welcome_text
        rooms_section
            room_section
                hotel_picture
                hotel_room_description
                    hotel_room_description_header
                        hotel_room_type
                        hotel_room_wheelchair_option
                    hotel_room_description_title
                    hotel_room_options
                        hotel_room_option_wifi
                        hotel_room_option_refreshments
                        hotel_room_option_tv
                        hotel_room_option_safe
                        hotel_room_option_radio
                        hotel_room_option_views
                    hotel_room_booking_button
                booker_contact_form
                    name_input_form
                    email_input_form
                    phone_input_form
                    subject_input_form
                    message_input_form
                    submit_button_on_contact_form
                    alert_booker_form
                hotel_contact_details_field
                map_picture
                footer_panel
                    site_owner_info
                    cookie_policy_link
                    privacy_policy_link
                    admin_panel_link
    ```

## Booking web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Booking web page: https://automationintesting.online](https://automationintesting.online/)

Same URL as for Home page but with additional components on the page

<img src="project_related_data\pic\restful-booker_site__book_this_room_page.png" alt="restful-booker_site__home_page_main.png" style="width:60%;">

## Admin side

### Admin (Rooms) web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Home web page: https://automationintesting.online/#/admin/](https://automationintesting.online/#/admin/)

<img src="project_related_data\pic\restful-booker_site__admin-room_page.png" alt="restful-booker_site__admin-room_page.png" style="width:70%;">

### Report web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Report web page: https://automationintesting.online/#/admin/report](https://automationintesting.online/#/admin/)

<img src="project_related_data\pic\restful-booker_site__report_page.png" alt="restful-booker_site__report_page.png" style="width:70%;">

### Branding web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Branding web page: https://automationintesting.online/#/admin/branding](https://automationintesting.online/#/admin/)

<img src="project_related_data\pic\restful-booker_site__branding_page.png" alt="restful-booker_site__branding_page.png" style="width:70%;">

### Messages web page

<a href="#toc" style="color: green;">go to TOC.</a>

[Messages web web page: https://automationintesting.online/#/admin/messages](https://automationintesting.online/#/admin/messages)

<img src="project_related_data\pic\restful-booker_site__messages_page.png" alt="restful-booker_site__messages_page.png" style="width:70%;">

# Test framework configuration and setup

## Required python packages

<a href="#toc" style="color: green;">go to TOC.</a>

In this project used 'pip-tools' and approach to use highlevel dependency tree. Main required packages presented in `requirements.in`. All used Python packages for the current project are generates in `requirements.txt`

Below is the list of main packages with references

### For tests itself

<a href="#toc" style="color: green;">go to TOC.</a>

* **pytest**
    * pypi.org docs: https://pypi.org/project/pytest/
    * related info: https://docs.pytest.org/en/latest/ 
    ```
    pip install pytest
    ```
  
* **hypothesis**
    * pypi.org docs: https://pypi.org/project/hypothesis/
    * related info: https://hypothesis.works/
    ```
    pip install hypothesis
    ```
  

### For ui/web testing

<a href="#toc" style="color: green;">go to TOC.</a>

* **selenium**
    * pypi.org docs: https://pypi.org/project/selenium/
    * related info: https://selenium-python.readthedocs.io/ 
    ```
    pip install selenium
    ```


* **webdriver-manager**
    * pypi.org docs: https://pypi.org/project/webdriver-manager/
    * related info:https://github.com/bonigarcia/webdrivermanager 
    ```
    pip install webdriver-manager
    ```

### Utils/configs

<a href="#toc" style="color: green;">go to TOC.</a>

* **mypy**
    * pypi.org docs: https://pypi.org/project/mypy/
    * related info: https://mypy-lang.org/
    ```
    pip install mypy
    ```

* **python-dotenv**
    * pypi.org docs: https://pypi.org/project/dotenv/
    * related info: https://www.dotenv.org/docs/languages/python
    ```
    pip install python-dotenv
    ```
  
* **pyyaml**
    * pypi.org docs: https://pypi.org/project/PyYAML/
    * related info: https://pyyaml.org/
    ```
    pip install pyyaml
    ```
  
* **configParser**
    * pypi.org docs: https://pypi.org/project/configparser/
    * related info: https://docs.python.org/3/library/configparser.html
    ```
    pip install configparser
    ```
  
* **openpyxl**
    * pypi.org docs: https://pypi.org/project/openpyxl/
    * related info: https://openpyxl.readthedocs.io/en/stable/
    ```
    pip install openpyxl
    ```

* **pylint**
    * pypi.org docs: https://pypi.org/project/pylint/
    * related info: https://github.com/pylint-dev/pylint
    ```
    pip install pylint
    ```
    
    Generate a default configuration file for the Pylint code analyzerby 
    ```
    pylint --generate-rcfile > pylint.rc
    ```

* **pyreverse**
    * pypi.org docs: https://pypi.org/project/pyreverse/
    * related info:  https://pylint.readthedocs.io/en/latest/pyreverse.html\
    Pyreverse has now been integrated to pylint : http://pypi.python.org/pypi/pylint/
    

* **pipdeptree**
    * pypi.org docs: https://pypi.org/project/pipdeptree/
    * related info: https://github.com/tox-dev/pipdeptree
    
    ```
    pip install pipdeptree
    ```
  
  
### Logging/reporting

* **allure**
    * pypi.org docs: https://pypi.org/project/allure-pytest/
    * related info: https://allurereport.org/docs/pytest/
    ```
    pip install allure-pytest
    ```

* **pytest-html**
    * pypi.org docs:https://pypi.org/project/pytest-html/
    * related info: https://pytest-html.readthedocs.io/en/latest/
    ```
    pip install pytest-html
    ```

* **loguru**
    * pypi.org docs: https://pypi.org/project/loguru/
    * related info: https://loguru.readthedocs.io/ 
    ```
    pip install loguru

### Data generators

<a href="#toc" style="color: green;">go to TOC.</a>

* **wonderwords**
    * pypi.org docs: https://pypi.org/project/wonderwords/
    * related info: https://loguru.readthedocs.io/
    ```
    pip install wonderwords
    ```

* **Faker**
    * pypi.org docs: https://pypi.org/project/Faker/
    * related info: http://faker.rtfd.org/
    ```
    pip install Faker
    ```

### DB
* **mysql-connector-python**
    * pypi.org docs: https://pypi.org/project/mysql-connector-python/
    * related info: https://dev.mysql.com/doc/connector-python/en/
    ```
    pip install mysql-connector-python
    ```

### Assertions

<a href="#toc" style="color: green;">go to TOC.</a>

* **PyHamcrest**
    * pypi.org docs: https://pypi.org/project/PyHamcrest/
    * related info: https://pyhamcrest.readthedocs.io/
    ```
    pip install PyHamcrest
    ```

* **regex**
    * pypi.org docs: https://pypi.org/project/regex/
    * related info: https://github.com/mrabarnett/mrab-regex
    ```
    pip install regex
    ```
### Code analysing

* pylint
      * pypi.org docs: https://pypi.org/project/pylint/
      * related info: https://pylint.readthedocs.io/en/latest/
    ```
    pip install pylint
    ```

# Project setup process
<a href="#toc" style="color: green;">go to TOC.</a>

## 0.Setup by scripts
By default you can use file: 
1. `setup_env.bat` for Windows-based machine or 
2. `setup_env.sh` UNIX-based
for validating python version, installing all packages required for running current project.
Otherwise you can manually install everything using described steps below or fix some issues that appears while project was configured via scripted file.  

## 1. Create and activate a new virtual environment:
<a href="#toc" style="color: green;">go to TOC.</a>

- **_Create virtual environment._**\
  Script below is creating environment with name 'env'.\
  If you want to create environment with unique name, please replace the env name using your env name in script\
  _python -m {here_is_your_venv_name} ../env_

  Working script for creating venv with name 'venv' is below:
    ```
    python -m venv ../env
    ```
  
  then activate it
    * for unix-based
  ```
  source ../venv/bin/activate
  ```
    * for windows
  ```
  .\.venv\Scripts\Activate
  ```

  If you like to have different name for the environment
  ```
  python -m venv {venv_for_project}   
  ```

  and then

  ```
  source {venv_for_project}/Scripts/activate
  ```

**_For deactivating created env use command_**\
    ```
    deactivate
    ```


## 2. Install required packages from requirements.txt
<a href="#toc" style="color: green;">go to TOC.</a>

```
pip install -r requirements.txt
```

If **_requirements.txt_** file is missing request, or you have different configuration of the project after installation, please generate new  _requirements.txt_ file using command\

`
pip-compile requirements.in
`
Created requirements.txt file will have all dependency for the project

In case if you are using 'pip-tools' do next steps, check requirements.in and do next actions. 
1. compile requirements.txt by

```
pip-compile requirements.in
```

2. install dependencies by

`
pip install -r requirements.txt  
`

## 3. Check prerequisites for Allure test report generation

<a href="#toc" style="color: green;">go to TOC.</a>

1. Check your system on installed and available :
   * JAVA
     ```
     java -version
     ```

   * Node.js
     ```
     node -v
     ```

     If programs are missing install them using info below

2. Install Java 3
    * Download Java 3 [HERE](https://nodejs.org/en/download/package-manager)

3. Install Node.js
    * Download Node.js [HERE](https://nodejs.org/en/download/package-manager)

4. In command prompt, run the below command
    ```
    npm install -g allure-commandline

5. Add _npm_ and _allure-commandline_ to system path
    ```
    %AppData\Roaming\npm
    ```
    %AppData\Roaming\npm\node_modules\allure-commandline\bin
   
6. Check that system can have access to allure by
    ```
    allure --version
    ```

7. Install allure-pytest
    ``` 
   pip install allure-pytest
    ```
   or from your IDE

## 4. Usage DB as source of test data

<a href="#toc" style="color: green;">go to TOC.</a>

In case if your test data is stored in DB or external files, check the project configuration and adjust test data
manually.

### 1. Update DB content

<a href="#toc" style="color: green;">go to TOC.</a>

If you are using data from DB generate data based on your testing model or paste it manually
preferable to use pip install mysql-connector-python
 
 
## Checking project dependency tree
### pipdeptree
Basic Dependency Tree
```python
pipdeptree
```
Dependency Tree in JSON Format
```python
pipdeptree --json
```
Dependency Tree with Outdated Packages
```python
pipdeptree --outdated
```
Dependency Tree for a Specific Package
```python
pipdeptree -p <package_name>
```
Generate a Text Report and Save to File
```python
pipdeptree > resources/project_dependencies.txt
```

Visualize Dependency Tree with Graphviz first install graphviz:
```python
pip install graphviz
```
then generate a graphical representation:
```python
pipdeptree --graph-output png > resources/project_dependencies.png
```

# Tests

<a href="#toc" style="color: green;">go to TOC.</a>

More information about test runs by pytest you can
find [here](https://pytest-with-eric.com/introduction/pytest-run-single-test/)

## Test execution by _pytest_

<a href="#toc" style="color: green;">go to TOC.</a>

All tests are located in **_tests_** folder

### Run all Tests

<a href="#toc" style="color: green;">go to TOC.</a>

To run all the tests from the root directory, you can use the following command:
```    
python pytest
```
or just
```python
pytest
```

You can add the -v flag to get more verbose output:

``` 
python pytest -v
```

![python_pytest_verbose.png](project_related_data/pic/python_pytest_verbose.png)

You can enable live console logging using the pytest -s command too.

### Run tests in a module

<a href="#toc" style="color: green;">go to TOC.</a>

To run all tests in a specific file (module), use the following command:

`pytest tests/unit/test_functions.py`

### Test run for specific test (by test name) by command

<a href="#toc" style="color: green;">go to TOC.</a>

Use the `-k` option followed by the name of the test function or method you want to run

`python -k {some_test}}`\
e.g.
```
python -k test_dummy_test.py
```

### Run tests in a directory

<a href="#toc" style="color: green;">go to TOC.</a>

Perhaps you may decide to split your tests by unit, integration, end-to-end, performance, regression and so on.\
If you need an overview of the various types of testing for your Python applications, this article on the types of\
software testing is a good introduction.\
In these cases it’s helpful to run tests within a specific directory, and you can use:

```
pytest {path_to_the_folder_with_test}
```

e.g.

```
pytest tests/dummy_tests
```

### Run tests by node IDs

<a href="#toc" style="color: green;">go to TOC.</a>

To run a specific test, you can use the test’s node ID, which is essentially its path in the syntax:\
`{filename.py}::{test_function_name}.`\
For example, to run the test_add_negative_numbers function in the test_functions.py file, you can use the following
command:

```
pytest  test/dummy_tests/test_functions.py::test_add_positive_numbers
```

This runs the **_test_add_positive_numbers_** test in the test_functions.py file.

### Run tests of a specific class

<a href="#toc" style="color: green;">go to TOC.</a>

You can also run all tests in a specific class. To do this, you use the :: operator followed by the class name.\
For example, to run all tests in the RegressionTests class, you can use the following command:

`pytest test/dummy_tests/test_functions.py::TestsUnit`

### Run tests by marker expressions

<a href="#toc" style="color: green;">go to TOC.</a>

By using markers, you can run specific groups of tests, exclude tests, and prioritize tests. This can help you to write
better tests and to get more value from your test suite.

We’ve covered several kinds of markers in the articles on Pytest Timeout, Pytest Skip Tests and Pytes Asyncio.

In Pytest, you can assign markers to your test functions using the @pytest.mark decorator. You can then use these
markers to run specific tests.

This is especially useful when you have different types of tests, such as fast and slow tests, and you want to run them
selectively.

Example of pytest written with markers presented below
```python
@pytest.mark.unit
def test_one():
    result_of_doing = do_something()
    assert result_of_doing ==1
```
To run tests based on marker expressions, you use the -m flag followed by the marker name.

```
[pytest]
markers =
    unit : unit tests
    end_to_end  : end to end tests
    skip : slow tests`
```
command is 

```
pytest -m unit
```

In case if ini file located not in the root directory marker should be passed via flag `-c` and valid configured path to
the ini file

## Additional parts for test run/configuration
### Specifying configuration file location

<a href="#toc" style="color: green;">go to TOC.</a>

The -c option allows you to specify the path to your pytest.ini file directly.

`pytest -c path/to/your/pytest.ini`\
example of usage for current project is ```pytest -c config/pytest.ini -m unit```

Better to set the PYTEST_ADDOPTS environment variable to include the config file path:

`export PYTEST_ADDOPTS="-c config/pytest.ini"`

### Rerun failed tests

```shell
pytest --reruns 3 --alluredir="resources/allure_reports
```
_Full Command Breakdown_

`-n 4`: Runs tests in parallel using 4 worker processes.

`--reruns 3`: Reruns any failed tests up to 3 times.

`--alluredir="resources/allure_reports"`: Specifies the directory to store Allure reports.

### Run tests in parallel(using workers)

**_Installing Required Plugins_**

Make sure you have the required plugins installed:
* for parallel test execution
```shell
pytest-xdist 
```
* for rerunning failed tests
```shell
pytest-rerunfailures 
```

```shell
pytest -n 3 
```
_-n 4_: Runs tests in parallel using 4 worker processes.


### Snippets for running existing tests

<a href="#toc" style="color: green;">go to TOC.</a>

1. Test for checking home page (not a booking view)

```
pytest test/web_app_tests/test_login_page.py::test_check_main_section_of_home_page
```

## Test report generation

<a href="#toc" style="color: green;">go to TOC.</a>

### By pytest (Simple Report)
Simple pytest report generation in html format is possible by executing command

Short Traceback:

```python
pytest --tb=short
```
Long Traceback (default):
```python
pytest --tb=long
```

No Traceback (only show test results):
```python
pytest --tb=short --disable-warnings
```

### By pytest (HTML Report)
```python
pytest --html=resources/test_report/project_test_report.html
```

### By pytest (JUnit XML Report)
```python
pytest --junitxml=resources/test_report/project_test_report.xml
```

### Test reports by Allure
<a href="#toc" style="color: green;">go to TOC.</a>

#### Creating initial pytest reports by Allure 
<a href="#toc" style="color: green;">go to TOC.</a>
For generating Allure reports on the tests performed, you must first execute tests by pytest.
You need specify a path for the test results directory in the --alluredir command-line argument when running your tests.

```shell
pytest --alluredir="resources/test_report/allure_reports"
```
If any any error appears 
* Check that the system statisfy Allure requirements.
* Confirm that all components installed, report folder is created.
 need to specify execution tests by pytests with specific output format. 

When test execution completed , Allure reports generation starts after executing
```shell
allure serve {path_to_report_folder}
```

Example of command execution:
```shell
(.venv) {project_dir_path} allure serve "resources/allure_reports"
```
command that is applicable for the current project configuration is
```shell
allure serve "resources/allure_reports"
```

After successful execution of command allure starts server and provide server URL for checking allure report in the browser.


## Existing(created) tests by categories
<a href="#toc" style="color: green;">go to TOC.</a>

### Test List
List of existing tests for the current project is possible to generate by executing python script `utilities/make_list_of_tests.py`\
Result will be presented in the `resources/list_of_all_project_tests.md`
All tests are grouping by categories. 
IMPORTANT!!!
If you did any changes, please validate path to the test dir in the `make_list_of_tests.py` 

# Resources for TA frameworks

<a href="#toc" style="color: green;">go to TOC.</a>

- [Contact List App - web app for pure API testing](https://thinking-tester-contact-list.herokuapp.com/)
    - was available at 18 June 2024
- Web apps for testing
  - [OrangeHRM web app](https://opensource-demo.orangehrmlive.com/)
  - [httpbin.org - web app](https://httpbin.org/#/)
      - was available at 18 June 2024
      - the developer - [Website](https://kennethreitz.org/)
      - A simple HTTP Request & Response Service.
      - Run locally: `$ docker run -p 80:80 kennethreitz/httpbin`
      - [HTML form](https://httpbin.org/forms/post) that posts to `/post /forms/post`
      - was available at 18 June 2024
  - [tutorialsninja.com - web app](https://tutorialsninja.com/demo/)
      - was available at 18 June 2024