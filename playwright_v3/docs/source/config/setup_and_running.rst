.. _setup_and_running:

===============
Setup & Running
===============

Install
=======

Dependencies are managed with ``pip-tools`` - the top-level list is
`requirements.in <../../../requirements.in>`_ and the pinned lock file
`requirements.txt <../../../requirements.txt>`_ is generated from it.

.. tabs::

   .. tab:: Bash / PowerShell (POSIX)

      .. code-block:: bash

         python -m venv .venv
         source .venv/bin/activate
         pip install -r requirements.txt

   .. tab:: Windows (cmd / PowerShell)

      .. code-block:: bat

         python -m venv .venv
         .venv\Scripts\activate
         pip install -r requirements.txt

To refresh the lock file after editing ``requirements.in``:

.. code-block:: bash

   pip-compile requirements.in

The bootstrap scripts (``setup_env.bat`` / ``setup_env.sh``) do the venv +
install in one step; ``setup_for_tox.bat`` also installs and runs ``tox``.

Installing Playwright browsers
==============================

After ``pip install -r requirements.txt``, install the browser binaries::

    playwright install firefox chromium --with-deps

This is a one-time step; binaries are cached by Playwright.  In CI,
``.github/workflows/ci.yml`` runs ``playwright install ${{ matrix.browser }} --with-deps``
per matrix job (Firefox and Chromium in parallel).

Run the tests
=============

The suite needs network access and the two live practice services.

.. code-block:: bash

   pytest -n auto            # full suite, in parallel (pytest-xdist)
   pytest -m api             # API tests only
   pytest -m ui --browser firefox   # UI tests (Playwright — see Installing Playwright browsers above)
   pytest -k booking         # by keyword
   pytest path/to/test.py::TestClass::test_name

Reports:

.. code-block:: bash

   tox -e test              # suite + Allure result directory
   pytest --cov=core --cov=utilities --cov-report=html      # coverage
   pytest --html=report.html --self-contained-html          # single-file HTML report
   pytest --alluredir=allure-results && allure serve allure-results

CI (``.github/workflows/ci.yml``) runs ``ruff`` lint and ``pytest`` with coverage on
every push and pull request.

.. important::

   ``pytest`` from the repo root loads ``pyproject.toml`` for its config
   (markers, ``testpaths``). There is no separate ``-c`` flag to pass.

Database as test data
=====================

The ``setup_database`` fixture (``resources/test_data/fixtures_api_test_data.py``)
creates an SQLite database at ``resources/test_data/test_data_for_ta_framework.db``
and seeds it with reference rows the first time it is called.  The fixture is
idempotent — running the suite multiple times does not duplicate rows.

The database is one of three intentional data sources in the framework (the
others being inline constants and the Excel workbook).  It demonstrates the
pattern of reading test data from a relational store; see
:class:`~utilities.excel_data_provider.ExcelDataProvider` for the Excel
equivalent.

To inspect the schema and seed data:

.. code-block:: bash

   sqlite3 resources/test_data/test_data_for_ta_framework.db ".tables"
   sqlite3 resources/test_data/test_data_for_ta_framework.db "SELECT * FROM login_test_data;"

Dependency tree
===============

To inspect the full dependency graph (all transitive dependencies):

.. code-block:: bash

   pip install pipdeptree
   pipdeptree

To export a PNG diagram:

.. code-block:: bash

   pipdeptree --graph-output png > deps.png

This is useful for auditing unexpected transitive dependencies or checking that
``requirements.txt`` is consistent with ``requirements.in``.
