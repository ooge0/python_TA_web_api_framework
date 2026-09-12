************
Environment
************

.. Important::
    Current project configured to use :term:`Tox` and a dedicated virtual environment via :term:`venv`.

Environment configuration
-------------------------

The project uses ``tox`` for isolated test execution and ``pip-tools`` to pin
dependencies.  The full dependency list is in ``requirements.in`` (top-level
declarations) and ``requirements.txt`` (compiled lock file).

Package categories
^^^^^^^^^^^^^^^^^^

**Test runner**

``pytest`` — core runner.
``pytest-xdist`` — parallel execution (``-n auto``).
``pytest-cov`` — coverage measurement.
``pytest-html`` — single-file HTML report.
``allure-pytest`` — Allure integration (decorators + result directory).

**Assertions**

``assertpy2`` — fluent assertion library.  Imported as
``from assertpy2 import assert_that, soft_assertions``.  Provides rich failure
messages and a ``with soft_assertions():`` context for non-fatal multi-checks.

**UI (Selenium)**

``selenium`` — WebDriver API.
``webdriver-manager`` — automatic driver download and caching.

**Data**

``faker`` — generates realistic fake data (names, emails, phone numbers).
``openpyxl`` — reads the ``.xlsx`` test-data workbook
(``resources/test_data/booker_test_data.xlsx``).
``jsonschema`` — validates ``/booking`` API responses against a JSON Schema.
``hypothesis`` — property-based fuzzing of auth payloads.

**API / HTTP**

``requests`` — all HTTP calls go through ``APIClient`` (a ``requests.Session``
wrapper).

**Logging and reporting**

``loguru`` — structured console and file logging; one log file per test run.

**Code quality**

``ruff`` — linter and formatter (replaces pylint).
``pydocstyle`` — docstring style checking.

**Configuration**

``pydantic`` / ``pydantic-settings`` — typed settings loaded from
``config/config.ini`` and environment variables.

**Documentation**

``sphinx`` — documentation generator.
``sphinx-rtd-theme`` — ReadTheDocs theme.
``sphinx-autoapi`` — API reference pages from source.
``myst-parser`` — include ``README_.md`` in Sphinx via MyST.
``sphinx-tabs`` — tabbed content blocks.
``rst2pdf`` — PDF export via ``tox -e make_pdf_docs``.

**Dev tooling**

``pip-tools`` — ``pip-compile`` generates ``requirements.txt`` from
``requirements.in``.
``tox`` — test environment orchestration (``py312``, ``lint``, ``test``,
``make_html_docs``, ``make_pdf_docs``).
``invoke`` — task runner for Sphinx builds (``python -m invoke build-html``).

.. admonition:: tox.ini

   .. literalinclude:: ../../../tox.ini
      :language: ini
      :linenos: