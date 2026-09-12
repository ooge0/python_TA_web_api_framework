.. _framework_structure_page:
Framework structure
=======================


Main directories
------------------
The main directories of the project are:

.. code-block:: text

   ├── core
   ├── config
   ├── resources
   ├── utilities
   └── tests

Each folder contains relevant modules for different testing functionalities.

Main components
--------------------

The test automation framework consists of the following main components:

- **UI Tests**: Automated browser tests using Selenium WebDriver.
- **API Tests**: RESTful API testing using the :ref:`Requests` library.
- **Backend Tests**: Database validation through direct queries.

.. warning::
   Make sure to configure the correct environment variables and database connections before running tests.
