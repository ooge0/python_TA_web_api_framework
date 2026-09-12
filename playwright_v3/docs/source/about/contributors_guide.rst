Notes for contributors
======================

Setup
-----

.. code-block:: bash

   python -m venv .venv
   .venv/Scripts/activate            # Windows;  source .venv/bin/activate on POSIX
   pip install -r requirements.txt

Dependencies are managed with ``pip-tools``: edit ``requirements.in``, then
``pip-compile requirements.in`` to refresh the lock file.

Running the checks
------------------

.. code-block:: bash

   pytest -n auto                    # the full suite, in parallel
   pytest -m api                     # API tests only
   pytest -m ui                      # UI tests (currently skipped - see roadmap M8)
   tox -e lint                       # pylint over core / utilities / tests
   tox -e test                       # suite + Allure results

CI (``.github/workflows/ci.yml``) runs ``pylint`` and ``pytest`` with coverage on
every push and pull request. ``pylint`` is reported but does not gate yet.

Conventions
-----------

* One assertion style per module (``assertpy2`` fluent ``assert_that`` is the default; ``soft_assertions()`` for multi-check blocks).
* API write tests must create and clean up their own data - no hard-coded ids.
* New test functions are auto-tagged ``api`` / ``ui`` by path; add a
  ``TC-*`` row in :ref:`qa_test_cases` and link the requirement.
* Docstrings: one accurate sentence beats a copy-pasted paragraph.
