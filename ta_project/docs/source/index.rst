.. python_TA_web_api_framework documentation master file.

.. figure:: /_static/images/logo_m.png
    :align: center
    :alt: Project Logo
    :figclass: align-center

    Where Python makes magic...

===========================
Python TA Web/API Framework
===========================

My hybrid test-automation framework for the *restful-booker* practice stack -
the UI and front-end API at `automationintesting.online
<https://automationintesting.online>`_ and the back-end API at
`restful-booker.herokuapp.com <https://restful-booker.herokuapp.com>`_.

I built it to practise assembling, documenting and publishing a framework end to
end. These docs are both the guide and my own reference.

.. contents::
   :local:
   :depth: 2
   :backlinks: top


Overview
========
What the framework is, how it is laid out, and the tools it uses.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Overview

   about/about_this_guide
   about/framework_structure
   about/features
   about/sut_description
   readme


Setup & Running
===============
Getting the framework installed and the suite running.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Setup & Running

   config/setup_and_running
   config/environment_setup
   config/running_tests
   config/sphinx_setup
   config/ci_cd


QA & Testing
============
The whole testing story in one section: what I test and how, a description of
what the tests check, the feature / requirements catalogue, the test cases with
their pytest node names, the traceability matrix, the coverage-by-feature view,
and the auto-generated reference for the test modules.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: QA & Testing

   qa/index


Decisions
=========
Architecture decision records — one page per non-obvious choice, with context,
decision and consequences.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Decisions

   decisions/index


Diagrams & Graphs
=================
Visualisations of the ``core`` package - class and package relationships and
how ``APIClient`` is wired.

.. toctree::
   :maxdepth: 2
   :caption: Diagrams & Graphs

   diagrams/graphs
   diagrams/classes_relationships
   diagrams/api_client_relationships
   diagrams/function_and_class_relationships


Contributors & FAQ
==================

.. toctree::
   :maxdepth: 2
   :caption: Contributors & FAQ

   about/contributors_guide
   about/faq


Reference
=========

.. toctree::
   :caption: Reference
   :glob:

   modindex
   glossary
