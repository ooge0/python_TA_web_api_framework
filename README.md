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

[Github repo]()

**_Test automation framework for testing UI, front-end and  back-end API of restful-booker web-site - [https://automationintesting.online](https://automationintesting.online)_.**

# Table of contents <div id="toc"></div>
1. [Resources of web app](#resources-of-web-app)
   1. [Restful-booker app resources](#restful-booker-app-resources)
      1. [Restful-booker web-site URL](#restful-booker-web-site-url)
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
3. [Project docs](#project-docs) 
4. [Project setup process](#project-setup-process)
   0. [Setup by scripts](#0setup-by-scripts) 
   1. [Create and activate a new virtual environment](#1-create-and-activate-a-new-virtual-environment)
   2. [Install required packages from requirements.txt](#2-install-required-packages-from-requirementstxt)
   3. [Check prerequisites for Allure test report generation](#3-check-prerequisites-for-allure-test-report-generation)
   4. [Usage DB as source of test data](#4-usage-db-as-source-of-test-data)
      1.  [Update DB content](#1-update-db-content)
   5. [Checking project dependency tree](#checking-project-dependency-tree)
      1. [pipdeptree](#pipdeptree)
   6. [Generating documentation by Sphinx](#generating-documentation-by-sphinx) 
5. [Tests](#tests) 
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
6[Resources for TA frameworks](#resources-for-ta-frameworks)


# Resources of web app
## Restful-booker app resources

### Restful-booker web-site URL
[https://automationintesting.online/](https://automationintesting.online/)

#### Restful-booker API
[https://restful-booker.herokuapp.com/apidoc/index.html](https://restful-booker.herokuapp.com/apidoc/index.html)

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

[Messages web page: https://automationintesting.online/#/admin/messages](https://automationintesting.online/#/admin/messages)

<img src="project_related_data\pic\restful-booker_site__messages_page.png" alt="restful-booker_site__messages_page.png" style="width:70%;">

# Test framework configuration and setup

## Required python packages

<a href="#toc" style="color: green;">go to TOC.</a>

In this project used 'pip-tools' and approach to use high-level dependency tree. Main required packages presented in `requirements.in`. All used Python packages for the current project are generates in `requirements.txt`

Below is the list of main packages with references

### For tests itself

<a href="#toc" style="color: green;">go to TOC.</a>
* **pytest**
    * pypi.org docs: [https://pypi.org/project/pytest/](https://pypi.org/project/pytest/)
    * related info: [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/) 
    ```bash
    pip install pytest
    ```

* **hypothesis**
    * pypi.org docs: [https://pypi.org/project/hypothesis/](https://pypi.org/project/hypothesis/)
    * related info: [https://hypothesis.works/](https://hypothesis.works/)
    ```bash
    pip install hypothesis
    ```

### For ui/web testing

[go to TOC](#toc)

* **selenium**
    * pypi.org docs: [https://pypi.org/project/selenium/](https://pypi.org/project/selenium/)
    * related info: [https://selenium-python.readthedocs.io/](https://selenium-python.readthedocs.io/) 
    ```bash
    pip install selenium
    ```

* **webdriver-manager**
    * pypi.org docs: [https://pypi.org/project/webdriver-manager/](https://pypi.org/project/webdriver-manager/)
    * related info: [https://github.com/bonigarcia/webdrivermanager](https://github.com/bonigarcia/webdrivermanager) 
    ```
    pip install webdriver-manager
    ```

### Utils/configs

[go to TOC](#toc)

* **mypy**
    * pypi.org docs: [https://pypi.org/project/mypy/](https://pypi.org/project/mypy/)
    * related info: [https://mypy-lang.org/](https://mypy-lang.org/)
    ```bash
    pip install mypy
    ```

* **python-dotenv**
    * pypi.org docs: [https://pypi.org/project/dotenv/](https://pypi.org/project/dotenv/)
    * related info: [https://www.dotenv.org/docs/languages/python](https://www.dotenv.org/docs/languages/python)
    ```bash
    pip install python-dotenv
    ```

* **pyyaml**
    * pypi.org docs: [https://pypi.org/project/PyYAML/](https://pypi.org/project/PyYAML/)
    * related info: [https://pyyaml.org/](https://pyyaml.org/)
    ```bash
    pip install pyyaml
    ```

* **configParser**
    * pypi.org docs: [https://pypi.org/project/configparser/](https://pypi.org/project/configparser/)
    * related info: [https://docs.python.org/3/library/configparser.html](https://docs.python.org/3/library/configparser.html)
    ```bash
    pip install configparser
    ```

* **openpyxl**
    * pypi.org docs: [https://pypi.org/project/openpyxl/](https://pypi.org/project/openpyxl/)
    * related info: [https://openpyxl.readthedocs.io/en/stable/](https://openpyxl.readthedocs.io/en/stable/)
    ```bash
    pip install openpyxl
    ```

* **pylint**
    * pypi.org docs: [https://pypi.org/project/pylint/](https://pypi.org/project/pylint/)
    * related info: [https://github.com/pylint-dev/pylint](https://github.com/pylint-dev/pylint)
    ```bash
    pip install pylint
    ```
    
    Generate a default configuration file for the Pylint code analyzer by 
    ```bash
    pylint --generate-rcfile > pylint.rc
    ```

* **pyreverse**
    * pypi.org docs: [https://pypi.org/project/pyreverse/](https://pypi.org/project/pyreverse/)
    * related info:  [https://pylint.readthedocs.io/en/latest/pyreverse.html](https://pylint.readthedocs.io/en/latest/pyreverse.html) 
  
    Pyreverse has now been integrated to pylint : [http://pypi.python.org/pypi/pylint/](http://pypi.python.org/pypi/pylint/)
    

* **pipdeptree**
    * pypi.org docs: [https://pypi.org/project/pipdeptree/](https://pypi.org/project/pipdeptree/)
    * related info: [https://github.com/tox-dev/pipdeptree](https://github.com/tox-dev/pipdeptree)
    
    ```bash
    pip install pipdeptree
    ```

* **invoke**
    * pypi.org docs: https://pypi.org/project/invoke/
    * related info: https://www.pyinvoke.org/
    
    ```bash
    pip install invoke
    ```

### Logging/reporting

* **allure**
    * pypi.org docs: [https://pypi.org/project/allure-pytest/](https://pypi.org/project/allure-pytest/)
    * related info: [https://allurereport.org/docs/pytest/](https://allurereport.org/docs/pytest/)
    ```bash
    pip install allure-pytest
    ```

* **pytest-html**
    * pypi.org docs: [https://pypi.org/project/pytest-html/](https://pypi.org/project/pytest-html/)
    * related info: [https://pytest-html.readthedocs.io/en/latest/](https://pytest-html.readthedocs.io/en/latest/)
    ```bash
    pip install pytest-html
    ```

* **loguru**
    * pypi.org docs: [https://pypi.org/project/loguru/](https://pypi.org/project/loguru/)
    * related info: [https://loguru.readthedocs.io/](https://loguru.readthedocs.io/) 
    ```bash
    pip install loguru
    ```

### Data generators

[go to TOC](#toc)

* **wonderwords**
    * pypi.org docs: [https://pypi.org/project/wonderwords/](https://pypi.org/project/wonderwords/)
    * related info: [https://loguru.readthedocs.io/](https://loguru.readthedocs.io/)
    ```bash
    pip install wonderwords
    ```

* **Faker**
    * pypi.org docs: [https://pypi.org/project/Faker/](https://pypi.org/project/Faker/)
    * related info: [http://faker.rtfd.org/](http://faker.rtfd.org/)
    ```bash
    pip install Faker
    ```

### DB
* **mysql-connector-python**
    * pypi.org docs: [https://pypi.org/project/mysql-connector-python/](https://pypi.org/project/mysql-connector-python/)
    * related info: [https://dev.mysql.com/doc/connector-python/en/](https://dev.mysql.com/doc/connector-python/en/)
    ```bash
    pip install mysql-connector-python
    ```

### Assertions

[go to TOC](#toc)

* **PyHamcrest**
    * pypi.org docs: [https://pypi.org/project/PyHamcrest/](https://pypi.org/project/PyHamcrest/)
    * related info: [https://pyhamcrest.readthedocs.io/](https://pyhamcrest.readthedocs.io/)
    ```bash
    pip install PyHamcrest
    ```

* **regex**
    * pypi.org docs: [https://pypi.org/project/regex/](https://pypi.org/project/regex/)
    * related info: [https://github.com/mrabarnett/mrab-regex](https://github.com/mrabarnett/mrab-regex)
    ```bash
    pip install regex
    ```

### Code analysing

* **pylint**
    * pypi.org docs: [https://pypi.org/project/pylint/](https://pypi.org/project/pylint/)
    * related info: [https://pylint.readthedocs.io/en/latest/](https://pylint.readthedocs.io/en/latest/)
    ```bash
    pip install pylint
    ```

# Project docs
This project contains generated documentation by Sphinx
All documentation you can find  by opening [index.html](docs/build/index.html) in the browser or check [ta_framework_ui_api.pdf](docs/pdf_docs/ta_framework_ui_api.pdf)
Sphinx setup and generating process described [here](#generating-documentation-by-sphinx)

# Project setup process
<a href="#toc" style="color: green;">go to TOC.</a>

## 0.Setup by scripts
By default, you can use file: 
1. `setup_env.bat` for Windows-based machine or 
2. `setup_env.sh` UNIX-based
for validating python version, installing all packages required for running current project.
Otherwise, you can manually install everything using described steps below or fix some issues that appears while project was configured via scripted file.  

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

**_For deactivating created env use command_**
*
    ```shell
    deactivate
    ```


## 2. Install required packages from requirements.txt
<a href="#toc" style="color: green;">go to TOC.</a>

```shell
pip install -r requirements.txt
```

If **_requirements.txt_** file is missing request, or you have different configuration of the project after installation, please check generate new  _requirements.txt_ file using command 

```shell
pip-compile requirements.in
```
Created `requirements.txt` file will have all dependency for the project.

In case if you are using 'pip-tools' do next steps, 
1. check `requirements.in` content for preventing conflicts with existing(venv/global) configurations. 
2. compile requirements.txt by

```shell
pip-compile requirements.in
```

3. install dependencies by

```shell
pip install -r requirements.txt  
```

## 3. Check prerequisites for Allure test report generation

<a href="#toc" style="color: green;">go to TOC.</a>

1. Check your system on installed and available :
   * JAVA
     ```shell
     java -version
     ```

   * Node.js
     ```shell
     node -v
     ```

     If programs are missing install them using info below

2. Install Java 3
    * Download Java 3 [HERE](https://nodejs.org/en/download/package-manager)

3. Install Node.js
    * Download Node.js [HERE](https://nodejs.org/en/download/package-manager)

4. In command prompt, run the below command
    ```shell
    npm install -g allure-commandline

5. Add _npm_ and _allure-commandline_ to system path
    ```shell
    %AppData\Roaming\npm
    ```
    %AppData\Roaming\npm\node_modules\allure-commandline\bin
   
6. Check that system can have access to allure by
    ```shell
    allure --version
    ```

7. Install allure-pytest
    ```shell
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
```shell
pipdeptree
```
Dependency Tree in JSON Format
```shell
pipdeptree --json
```
Dependency Tree with Outdated Packages
```shell
pipdeptree --outdated
```
Dependency Tree for a Specific Package
```shell
pipdeptree -p <package_name>
```
Generate a Text Report and Save to File
```shell
pipdeptree > resources/project_dependencies.txt
```

Visualize Dependency Tree with Graphviz first install graphviz:
```shell
pip install graphviz
```
then generate a graphical representation:
```shell
pipdeptree --graph-output png > resources/project_dependencies.png
```
## Documentation

## Pydocstyle
To check your code for missing docstrings for current project selected pydocstyle.

```bash
pydocstyle core
````
### 3. **Check an Entire Directory**

To check all Python files in a specific directory, you can run:

bash
`pydocstyle path/to/your_directory/`

### 4. **Check with Specific Conventions**

You can specify the docstring conventions you want to enforce using the `--convention` flag. The available conventions are:

- `google`
- `numpy`
- `pep257`

For example, to check using the Google style:

bash
`pydocstyle --convention=google path/to/your_directory/`

### 5. **Ignore Specific Errors**

If you want to ignore certain error codes, you can use the `--ignore` option followed by the error codes (comma-separated). For example, to ignore error code D103 (missing docstring in public function):

bash
`pydocstyle --ignore=D103 path/to/your_directory/`

### 6. **Output Format**

You can change the output format using the `--format` option. The default format is a simple text output, but you can change it to `json` for easier parsing:

bash
`pydocstyle --format=json path/to/your_directory/`

### 7. **Verbose Mode**

To see more detailed output, you can run `pydocstyle` in verbose mode:

bash
`pydocstyle --verbose path/to/your_directory/`

### 8. **Checking a Specific File or Line**

You can check a specific line in a file by appending the line number to the file path. For example, to check line 42 of `your_file.py`:

bash
`pydocstyle path/to/your_file.py:42`

### 9. **Show Available Error Codes**

To see a list of all available error codes and their meanings, use the `--help` option:

bash
`pydocstyle --help`

### Summary of Commands

- **Check a specific file**:
    
    ```bash
    pydocstyle path/to/your_file.py
    ```
    
- **Check an entire directory**:
    
    ```bash
    pydocstyle path/to/your_directory/
    ```
    
- **Specify conventions**:
    
    ```bash
    pydocstyle --convention=google path/to/your_directory/
    ```
    
- **Ignore specific errors**:
    
    ```bash
    pydocstyle --ignore=D103 path/to/your_directory/
    ```
    
- **Output in JSON format**:
    
    ```bash
    pydocstyle --format=json path/to/your_directory/
    ```

### Generating documentation by Sphinx
1. Install Sphinx in your project environment:

```bash
pip install sphinx
```

2. Set Up Sphinx in Your Project
	**!!! IMPORTANT** 
    For more convenient usage of project structure to better create separate folder where will be stored all documentation and related Sphinx config files and folder. \
    For this project was created new folder `docs` and from that place all Sphinx related command should be executed.
    After navigation to the `docs` directory, run:
    ```bash
    sphinx-quickstart
    ```
This command will guide you through setting up Sphinx by asking several configuration questions.

Typical responses:
* **Separate source and build directories**: Yes
* **Project name**: [Your project name]
* **Author name**: [Your name]
* **Project version**: [Your project version]
* **Project language**: [en]

    This will generate\
        1. `source/` directory with a default `conf.py` file for configuration and some starter `.rst` (reStructuredText) files.\
        2.  `build/` directory (will be empty). It's default directory that will have all project related data if you will not use any different name for collecting generated Sphinx docs (pdf, html... etc).  
          It can be deleted or renamed if you want to have separate places for different types of generated docs. For this project will be generated documentation in HTML and PDF formats. Below you will find scripts and instructions for generating documents in PDF and HTML format using different Sphinx extensions. 
        3. make.bat - default script file for generating docs on Windows OS
        4. Makefile - default script file for generating docs on UNIX base OS


3. Configure conf.py
Edit the generated [conf.py](docs/source/conf.py) file located in the source/ directory to customize your documentation. Key configurations to include:

	* **_Extensions_**: Enable useful Sphinx extensions, such as autodoc for auto-generating documentation from your Python docstrings:

    ```python
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',  # For Google-style or NumPy-style docstrings
    ]
    ```
* **_Paths_**: Set the path for your Python modules to be included in the docs:

    ```python
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../..'))
    ```
  
('../..')) line tells Python to add the parent directory (two levels up) to the Python module search path. This is necessary when your project's files (modules, packages, etc.) are in a directory separate from the documentation (Sphinx docs) directory.

By specifying ../.., you're telling Sphinx (and Python) to include the top-level project directory in its search path, allowing it to find and import modules from the project directory while building the documentation.

* **_HTML Theme_**: You can set the theme for your HTML documentation (default is alabaster):
    ```python
    html_theme = 'sphinx_rtd_theme'  # Example: ReadTheDocs theme
    ```
* **Source file suffix***: Define which file extensions to look for:

    ```python
    source_suffix = ['.rst', '.md']
    ```
4. Install related to chosen Sphinx extensions packages. 
   1. For 'sphinx_rtd_theme' theme execute

       ```bash
       pip install sphinx_rtd_theme
       ```
   2. For 'myst_parser' theme execute

       ```bash
       pip install myst_parser
       ```

   3. For 'rst2pdf' theme execute

       ```bash
       pip install rst2pdf
       ```


4. Document Your Code.

5. Generate reStructuredText (.rst) Files
To automatically generate `.rst` files from your Python code, use sphinx-apidoc. 
This will generate a `source/` directory with .rst files that describe your modules and classes:

    ```bash
    sphinx-apidoc -o source/ path/to/your/module
    ```
   **!!! IMPORTANT**\
   For the current project all Sphinx documentation is stored in `docs` folder and script below should be executed from the project root folder

    ```bash
    sphinx-apidoc -o docs/source .
    ```

6. Build HTML Documentation

    **!!! IMPORTANT**\
    **For the current project script below should be executed from the project root folder.**\
    Once your `.rst` files are in place and `conf.py` is configured, you can build the HTML documentation:
    
   * on Windows OS 
     ```bash
     sphinx-build -b html docs/source/ docs/html_docs/
     ```
     where **_html_docs_** - custom defined name for storing generated html docs.
    
       If errors appears after generating docs try to clear the cached build.\
       Clear the `build/` directory by deleting it or running: 
       
        ```bash
        sphinx-build -b html -E source/ html_docs/
        ````
        The -E flag forces Sphinx to rebuild everything from scratch, avoiding potential caching issues.
    
   * on UNIX
       ```bash
       make html
       ```
     This command will generate the HTML files inside the build/html/ directory. Open the `index.html` file in your browser to view your documentation.
    
7. Build PDF Documentation
 
* on Windows OS 
    ```bash
    sphinx-build -b pdf source/ pdf_docs/
    ```


8. View Documentation
Navigate to the build/html/ directory and open index.html in your browser to view your generated documentation.

Additional Configurations (Optional)
Include Markdown files: If you want to include .md files, ensure the myst_parser is installed and enabled:

```bash
	pip install myst-parser
```

Then add it to `conf.py`:

```python
	extensions = ['myst_parser']
```
Customizing Themes: You can install additional Sphinx themes by running pip install <theme-name> and configuring html_theme in `conf.py`.

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
```shell 
python pytest
```
or just
```shell
pytest
```

You can add the -v flag to get more verbose output:

```shell 
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

`python -k {some_test}}` e.g. `python -k test_dummy_test.py`

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

```shell
pytest tests/dummy_tests
```

### Run tests by node IDs

<a href="#toc" style="color: green;">go to TOC.</a>

To run a specific test, you can use the test’s node ID, which is essentially its path in the syntax:\
`{filename.py}::{test_function_name}.`\
For example, to run the test_add_negative_numbers function in the test_functions.py file, you can use the following
command:

```shell
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
```
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
Rerun for failed tests work after installation of `pytest-rerunfailures` 

```shell
pip install pytest-rerunfailures
```
Check version of `pytest-rerunfailures`
```shell
pytest-rerunfailures --version
```

```shell
pytest --reruns 3 --alluredir="resources/project_test_reports/allure_reports
```
or in paralel
```shell
pytest  -n 10 --reruns 3 --alluredir="resources/project_test_reports/allure_reports"
```
_Full Command Breakdown_

`-n 10`: Runs tests in parallel using 10 worker processes.

`--reruns 3`: Reruns any failed tests up to 3 times.

`--alluredir="resources/project_test_reports/allure_reports"`: Specifies the directory to store Allure reports.

### Run tests in parallel(using workers)

**_Installing Required Plugins_**

Make sure you have the required plugins installed:
* for parallel test execution`pytest-xdist`

```shell
pytest -n 3 
```
_-n 4_: Runs tests in parallel using 4 worker processes.


### Snippets for running existing tests

<a href="#toc" style="color: green;">go to TOC.</a>

1. Test for checking home page (not a booking view)

```shell
pytest test/web_app_tests/test_login_page.py::test_check_main_section_of_home_page
```

## Test report generation

<a href="#toc" style="color: green;">go to TOC.</a>

### By pytest (Simple Report)
Simple pytest report generation in html format is possible by executing command

Short Traceback:

```shell
pytest --tb=short
```
Long Traceback (default):
```shell
pytest --tb=long
```

No Traceback (only show test results):
```shell
pytest --tb=short --disable-warnings
```

### By pytest (HTML Report)
```shell
pytest --html=resources/project_test_reports/pytest_reports/pytest_general_test_report.html
```
using workers
```shell
pytest -n 10 --html=resources/project_test_reports/pytest_html_reports/pytest_html_general_test_report.html
```

### By pytest (JUnit XML Report)
```shell
pytest --junitxml=resources/project_test_reports/pytest_junit_xml_reports/pytest_junit_xml_general_test_report.xml
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
```
allure serve {path_to_report_folder}
```

Example of command execution:
```
(.venv) {project_dir_path} allure serve "resources/allure_reports"
```
command that is applicable for the current project configuration is
```shell
allure serve "resources/test_report/allure_reports"
```

After successful execution of command allure starts server and provide server URL for checking allure report in the browser.


## Existing(created) tests by categories
<a href="#toc" style="color: green;">go to TOC.</a>

### Test List
List of existing tests for the current project is possible to generate by executing python script [make_list_of_tests.py](utilities/make_list_of_tests.py).
Result will be presented in the [list_of_all_project_tests.md](resources/list_of_all_project_tests.md). \
All tests are grouping by categories. \
IMPORTANT!!!
If you did any changes, please validate path to the test dir in the [make_list_of_tests.py](utilities/make_list_of_tests.py) 

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