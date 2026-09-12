.. _config_ci_cd:

======================
CI/CD pipeline
======================

Two GitHub Actions workflows automate testing, linting and documentation
publishing.  Both live under ``.github/workflows/``.

.. contents::
   :local:
   :depth: 2


Continuous integration — ``ci.yml``
====================================

Triggers: every push, every pull request, and manual ``workflow_dispatch``.
Concurrency is grouped by ref (``ci-${{ github.ref }}``) with
``cancel-in-progress: true``, so a new push cancels any in-flight run on the
same branch.

The workflow has six jobs:

1. **lint** — installs dependencies, runs ``ruff check`` on ``core``,
   ``utilities`` and ``tests``.

2. **traceability** — runs
   ``python -m utilities._devtools.check_traceability``.  The script collects
   every ``@pytest.mark.req("REQ-...")`` marker, diffs it against the
   requirements catalogue and exits non-zero if any requirement is uncovered.
   This is the CI enforcement side of :ref:`qa_other_signals`.

3. **docs** — builds Sphinx HTML with ``sphinx-build -b html docs/source
   docs/_build/html -W --keep-going`` (warnings as errors).  On completion the
   built site is uploaded as the ``sphinx-html`` artifact.

4. **test-api** — runs the API suite in parallel:

   .. code-block:: text

      pytest -n auto -m "not ui" \
        --cov --cov-report=term-missing --cov-report=xml \
        --junitxml=junit-api.xml \
        --alluredir=allure-results-api

   Uploads three artifacts: ``api-test-reports`` (JUnit XML + coverage XML)
   and ``allure-results-api``.  A ``dorny/test-reporter`` step renders the
   JUnit XML as a PR check annotation so individual failures appear inline in
   the PR diff.

5. **test-ui** — runs the UI suite in a **browser matrix** (Firefox + Chromium):

   .. code-block:: yaml

      strategy:
        fail-fast: false
        matrix:
          browser: [firefox, chromium]

   Each matrix job installs its browser binary::

      playwright install ${{ matrix.browser }} --with-deps

   then runs:

   .. code-block:: text

      pytest -m ui -n0 --browser ${{ matrix.browser }} \
        --junitxml=junit-ui-${{ matrix.browser }}.xml \
        --screenshot only-on-failure \
        --video retain-on-failure \
        --tracing retain-on-failure \
        --alluredir=allure-results-ui-${{ matrix.browser }}

   Uploads ``ui-test-reports-<browser>`` (JUnit XML) and
   ``allure-results-ui-<browser>`` per browser.  No geckodriver or
   ``setup-firefox`` action is needed — Playwright manages its own binaries.

6. **allure-report** — runs after both test jobs (``if: always()``).
   Downloads ``allure-results-api`` and ``allure-results-ui`` into a single
   ``allure-results/`` directory, then generates a combined HTML report via
   ``simple-elf/allure-report-action@v1.9``.  The report is uploaded as the
   ``allure-report`` artifact.


Documentation deployment — ``deploy-docs.yml``
================================================

Triggers: push to ``master`` and manual ``workflow_dispatch``.

Two jobs:

1. **build** — checks out the repo, installs dependencies from
   ``requirements.txt``, builds Sphinx HTML into ``docs/_build/html``, and
   uploads the result via ``actions/upload-pages-artifact``.

2. **deploy** — deploys the uploaded artifact to GitHub Pages via
   ``actions/deploy-pages``.  The deployed URL is set by the ``github-pages``
   environment.

Concurrency group ``pages`` with ``cancel-in-progress: false`` ensures only
one Pages deployment runs at a time without cancelling a running one.


Artifacts produced
==================

.. list-table::
   :header-rows: 1
   :widths: 28 20 52

   * - Artifact name
     - Produced by
     - Contents
   * - ``sphinx-html``
     - docs
     - Built Sphinx HTML site
   * - ``api-test-reports``
     - test-api
     - ``junit-api.xml``, ``coverage.xml``
   * - ``allure-results-api``
     - test-api
     - Raw Allure JSON results (API suite)
   * - ``ui-test-reports-firefox``
     - test-ui (firefox)
     - ``junit-ui-firefox.xml``
   * - ``ui-test-reports-chromium``
     - test-ui (chromium)
     - ``junit-ui-chromium.xml``
   * - ``allure-results-ui``
     - test-ui
     - Raw Allure JSON results (UI suite)
   * - ``allure-report``
     - allure-report
     - Combined Allure HTML report (API + UI)


PR annotations
==============

Both test jobs use ``dorny/test-reporter@v1`` with ``reporter: java-junit``.
When a test fails in a pull request, the reporter posts a check-run summary
and annotates the failing test file and line directly in the PR diff view.

The ``name`` field distinguishes the two: *API test results* and
*UI test results*.


Status badges
=============

The README carries two workflow badges:

.. code-block:: text

   [![CI](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/ci.yml/badge.svg)]
   [![Docs](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/deploy-docs.yml/badge.svg)]

They reflect the latest run on the default branch.


Key configuration notes
========================

1. **Python version** — both workflows pin ``3.12``.
2. **Dependency caching** — ``actions/setup-python`` with ``cache: pip``.
3. **Timeout** — test jobs have ``timeout-minutes: 15``.
4. **Browser matrix** — the UI job runs Firefox and Chromium as parallel matrix
   jobs.  Each test gets an isolated browser context so there is no shared-state
   race and no ``-n0`` constraint between test workers within a job.
5. **Allure merge** — the allure-report job downloads both result sets into
   the same directory before generation, so the final report covers the full
   suite.
6. **Sphinx strict mode** — the docs job uses ``-W --keep-going`` so any
   Sphinx warning is a build error but all warnings are reported before
   failing.
