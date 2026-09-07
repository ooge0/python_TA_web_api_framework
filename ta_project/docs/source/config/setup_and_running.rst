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

Run the tests
=============

The suite needs network access and the two live practice services.

.. code-block:: bash

   pytest -n auto            # full suite, in parallel (pytest-xdist)
   pytest -m api             # API tests only
   pytest -m ui              # UI tests (currently skipped - roadmap M8)
   pytest -k booking         # by keyword
   pytest path/to/test.py::TestClass::test_name

Reports:

.. code-block:: bash

   tox -e test              # suite + Allure result directory
   pytest --cov=core --cov=utilities --cov-report=html      # coverage
   pytest --html=report.html --self-contained-html          # single-file HTML report
   pytest --alluredir=allure-results && allure serve allure-results

CI (``.github/workflows/ci.yml``) runs ``pylint`` and ``pytest`` with coverage on
every push and pull request.

.. important::

   ``pytest`` from the repo root loads ``pyproject.toml`` for its config
   (markers, ``testpaths``). There is no separate ``-c`` flag to pass.
