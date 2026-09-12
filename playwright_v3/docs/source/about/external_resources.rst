.. _about_external_resources:

==================
External resources
==================

Practice applications
=====================

`restful-booker <https://restful-booker.herokuapp.com>`_
   The back-end API under test.  Provides ``/auth``, ``/booking``, ``/room``,
   ``/branding``, ``/message``, ``/report`` and ``/ping`` endpoints.
   `API docs <https://restful-booker.herokuapp.com/apidoc/index.html>`_.

`restful-booker-platform <https://automationintesting.online>`_
   The full-stack practice application (React SPA + REST API) that this
   framework uses for both front-end API and UI testing.  The admin area is at
   ``/admin``; the public front page at ``/``.

Other practice applications (referenced in the framework as alternatives)
   - `Contact List App <https://thinking-tester-contact-list.herokuapp.com>`_
   - `OrangeHRM <https://opensource-demo.orangehrmlive.com>`_
   - `httpbin.org <https://httpbin.org>`_ — HTTP echo/inspect service
   - `tutorialsninja.com <https://tutorialsninja.com/demo/>`_ — e-commerce demo

QA documentation standards
===========================

`ISTQB Foundation syllabus <https://www.istqb.org/>`_
   Test design techniques, traceability, test plan templates.

`ISO/IEC/IEEE 29119-3 <https://softwaretestingstandard.org/>`_
   Test documentation standard; the test plan and test-case structure in this
   framework follows its recommendations.

`Ministry of Testing <https://www.ministryoftesting.com/>`_
   Guidance on writing test cases and traceability matrices.

Tools and libraries
===================

`pytest <https://docs.pytest.org/>`_
   Test runner.

`Allure Framework <https://allurereport.org/docs/pytest/>`_
   Test reporting with ``@allure.epic`` / ``@allure.feature`` / ``@allure.story``
   labels and per-test attachments.

`Playwright <https://playwright.dev/python/docs/intro>`_
   Browser automation for the UI tests (v3). Provides built-in auto-wait,
   network interception, browser contexts, and cross-browser support
   (Chromium, Firefox, WebKit) in a single API.

`assertpy2 <https://pypi.org/project/assertpy2/>`_
   Fluent assertion library: ``assert_that(x).is_equal_to(y)``, soft assertions.

`Hypothesis <https://hypothesis.readthedocs.io/>`_
   Property-based fuzzing; used for the auth payload fuzz test.

`Faker <https://faker.readthedocs.io/>`_
   Generates realistic fake data for booking, contact and room payloads.

`Sphinx <https://www.sphinx-doc.org/>`_
   Documentation generator that builds these pages.

`ruff <https://docs.astral.sh/ruff/>`_
   Linter and formatter (replaces pylint/flake8/isort).

`pip-tools <https://pip-tools.readthedocs.io/>`_
   Compiles ``requirements.in`` into a pinned ``requirements.txt``.
