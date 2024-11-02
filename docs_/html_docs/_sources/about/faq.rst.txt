FAQ
===

This FAQ section provides answers to common questions regarding the Python Test Automation Framework using `pytest`, `tox`, and `allure`.

**Table of Contents**

.. contents::
   :local:

**1. How do I install all required dependencies for the test automation framework?**
________________________________________________________________________________________

To install all the required dependencies, simply run the following command from the root of your project:

.. code-block:: bash

    pip install -r requirements.txt

Make sure your `requirements.txt` file lists all the necessary packages, such as `pytest`, `tox`, `allure-pytest`, and any other libraries.


**2. How can I run the tests using `pytest`?**
________________________________________________________________________________________

To execute the tests, run the following command from the project's root directory:

.. code-block:: bash

    pytest --alluredir=./allure-results

This will run all tests in the project and generate the test results in the `allure-results` folder.

**3. How can I generate a test report using `allure`?**
________________________________________________________________________________________

After running the tests, generate an Allure report with the following command:

.. code-block:: bash

    allure serve ./allure-results

This will launch a local server and display the test results in the browser.

**4. What is the purpose of `tox` in the framework?**
________________________________________________________________________________________

`tox` is used to automate testing in multiple environments. It ensures that your tests work across different Python versions and dependencies. To run tests in multiple environments, configure the `tox.ini` file and use:

.. code-block:: bash

    tox

`tox` will create virtual environments and run your tests in all configured environments.

**5. How do I run tests in parallel using `pytest-xdist`?**
________________________________________________________________________________________

To speed up test execution by running tests in parallel, use the following command with `pytest-xdist`:

.. code-block:: bash

    pytest -n <number_of_processes>

For example, to run the tests with 4 processes:

.. code-block:: bash

    pytest -n 4

**6. How can I skip tests conditionally?**
________________________________________________________________________________________

You can conditionally skip tests based on various conditions using the `pytest.mark.skipif` decorator. For example, to skip a test if the Python version is below 3.6:

.. code-block:: python

    import sys
    import pytest

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
    def test_function():
        assert True

**7. What is the correct way to structure my tests in the framework?**
________________________________________________________________________________________

It's a good practice to organize your tests in a clear and modular manner. A typical structure is:

.. code-block:: text

    ├── tests/
    │   ├── ui/
    │   ├── api/
    │   └── backend/
    ├── core/
    ├── config/
    ├── requirements.txt
    └── tox.ini

Each folder under `tests/` corresponds to a different part of the application being tested, such as UI, API, or backend.

**8. How can I rerun failed tests automatically?**
________________________________________________________________________________________

You can configure pytest to automatically rerun failed tests using the `pytest-rerunfailures` plugin. Install the plugin with:

.. code-block:: bash

    pip install pytest-rerunfailures

Then, add the `--reruns` option to rerun tests. For example, to rerun failed tests up to 3 times:

.. code-block:: bash

    pytest --reruns 3

**9. How can I filter tests by markers or test names?**
________________________________________________________________________________________

To run only tests marked with a specific marker (e.g., `slow`), use:

.. code-block:: bash

    pytest -m slow

To run a specific test or tests by name, use:

.. code-block:: bash

    pytest -k "test_name"

This allows you to filter tests by substring matching within test names.

**10. How do I integrate the framework with CI/CD pipelines?**
________________________________________________________________________________________

To integrate with CI/CD, such as GitHub Actions, Jenkins, or GitLab CI, configure your pipeline to install dependencies, run tests with `pytest`, and generate an Allure report. An example GitHub Actions YAML snippet is:

.. code-block:: yaml

    name: CI

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout code
          uses: actions/checkout@v2
        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: 3.8
        - name: Install dependencies
          run: |
            pip install -r requirements.txt
        - name: Run tests
          run: |
            pytest --alluredir=./allure-results
        - name: Upload Allure Results
          uses: actions/upload-artifact@v2
          with:
            name: allure-results
            path: ./allure-results

