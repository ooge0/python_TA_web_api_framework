.. ta_framework_ui_api documentation master file created by sphinx-quickstart.

.. figure:: /_static/images/logo_m.png
    :align: center
    :alt: Project Logo
    :figclass: align-center

    Where Python makes magic...

=========================
Python TA Framework Docs
=========================

Welcome to the Python Hybrid Test Automation Framework documentation!

This project focuses on testing the UI, front-end, and back-end API of restful-booker web-site: `<https://automationintesting.online>`_

For more details about the web site that is using for tests please, visit `<https://www.ministryoftesting.com/>`_.

-------------------------


**Table of Contents**

.. contents::
   :local:
   :depth: 3
   :backlinks: top


Project Overview
================
This section includes high-level information about the project, including framework components, setup instructions, and key features.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Overview

   about/about_this_guide
   readme
   about/framework_structure
   about/features


Framework Setup
===============
This section contains Instructions for setting up the project, installing dependencies, configuring test environments and running tests.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Setup Guide

   about/installation_guide
   config/environment_setup
   config/virtual_env
   config/running_tests


Tests
=====
This section contains details about the UI, API, and backend tests included in the framework.
In teh current project used `pytest` framework approach and all related information about packages, test, some helpful information you can find below.


.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Test Details

   tests/tests


Diagrams and Graphs
===================
This section contains visualization of framework components, relationships, and dependencies. Most important part is in `core` package and here you can find detailed description on how it was built and used in UI/API tests.

.. toctree::
   :maxdepth: 2
   :caption: Diagrams and Graphs

   diagrams/graphs
   diagrams/classes_relationships
   diagrams/api_client_relationships
   diagrams/function_and_class_relationships


Additional Notes
================
This section was created for contributors, guidelines, and troubleshooting.

.. toctree::
   :maxdepth: 2
   :caption: Contributors and FAQ

   about/contributors_guide
   about/faq

Module Index
=============
Here you can find references on most important python modules (files) that is used in the project.

.. toctree::
   :caption: Python Module Index
   :numbered:
   :glob:

   modindex


Glossary
=============

.. toctree::
   :maxdepth: 2
   :glob:
   :caption: Glossary

   glossary

Glossary section contains most important references and terms that are used in the project.
My focus was concentrated on basics and building clear and short references for most important entities of the project.

