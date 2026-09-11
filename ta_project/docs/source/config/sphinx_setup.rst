.. _sphinx_setup:

====================
Sphinx Documentation
====================

How the documentation is built and published.

Prerequisites
=============

The documentation dependencies are in ``requirements.txt`` (pulled from
``requirements.in``):

#. ``sphinx``
#. ``sphinx_rtd_theme``
#. ``myst-parser`` (for ``.md`` includes)
#. ``rst2pdf`` (PDF output)
#. ``sphinx-autoapi`` and ``sphinx.ext.autosummary`` (API reference)

Configuration
=============

``docs/source/conf.py`` is the Sphinx configuration.  Key settings:

* ``extensions``: autodoc, autosummary, autoapi, napoleon, myst_parser,
  rst2pdf, graphviz, viewcode, intersphinx.
* ``sys.path.insert(0, ...)`` adds the project root so autodoc can import
  modules.
* ``html_theme = 'sphinx_rtd_theme'``.
* ``source_suffix = ['.rst', '.md']``.

Building HTML
=============

From the project root:

.. code-block:: bash

   sphinx-build -b html docs/source docs/html

Or through tox / invoke:

.. code-block:: bash

   tox -e make_html_docs
   python -m invoke build-html

The output lands in ``docs/html/``.  Open ``docs/html/index.html`` to view.

To force a clean rebuild (ignore cached doctrees):

.. code-block:: bash

   sphinx-build -b html -E docs/source docs/html

Building PDF
============

.. code-block:: bash

   sphinx-build -b pdf docs/source docs/pdf_docs

Or:

.. code-block:: bash

   tox -e make_pdf_docs

Publishing to GitHub Pages
==========================

The project uses a committed ``docs/html/`` directory on the ``gh-pages``
branch.  The workflow:

#. Build HTML locally (see above).
#. Commit the output to ``gh-pages``.
#. GitHub Pages serves from that branch.

A GitHub Actions workflow (``deploy-docs.yml``) exists but is not currently
active; the manual approach is used instead.

ReadTheDocs
===========

The docs are also published on ReadTheDocs at
`python-ta-web-api-framework.readthedocs.io
<https://python-ta-web-api-framework.readthedocs.io/en/latest/index.html>`_.
