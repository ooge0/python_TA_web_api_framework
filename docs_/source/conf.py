import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ta_framework_ui_api'
copyright = '2024, si0n4ra'
author = 'si0n4ra'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# ---------------------- Extensions ------------------------
extensions = [
    'sphinx.ext.autodoc',           # For automatic class/method documentation
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',       # This can help with summarizing
    'myst_parser',                  # markDown parser
    'sphinx.ext.viewcode',          # To include links to source code
    'sphinx.ext.graphviz',          # For Graphviz support
    'sphinx_autodoc_typehints',     # For type hints support
    'rst2pdf.pdfbuilder',           # for making PDF docs
    'sphinx.ext.inheritance_diagram',      #  <<< !!!!
    'autoapi.extension',
    'sphinx.ext.duration', # extension measures durations of Sphinx processing and show its result at end of the build. It is useful for inspecting what document is slowly built
    'sphinx_tabs.tabs', # for rendering tables from the source code in rst files
    'notfound.extension', # Create a custom 404 page with absolute URLs hardcoded.

]

# ------------------- SOURCE FILE SUFFIXES ----------------------------

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []
locale_dirs = []     # Disable translations if not required



# -------------  Indexing -------------------
# Enable module index
html_use_modindex = True

# Enable general index
html_use_index = True

# ----- auto API configs -----------------------------

autoapi_dirs = ['../../core', '../../config', '../../utilities', '../../resources', '../../tests']   # Add both core and tests directories
autoapi_type = 'python'
autoapi_generate_api_docs = False
autoapi_add_toctree_entry = False                   # Avoids adding entries to the main toctree
autoapi_python_class_content = "both"               # Include both class docstring and methods
autosummary_generate = True                         # Allow to create auto summary for project

## Snippet for deafult configuration of autodoc
# autodoc_default_options = {
#     'members': True,
#     'undoc-members': True,
#     'private-members': False,
#     'special-members': False,
#     'inherited-members': True,
#     'show-inheritance': True,
#     'recursive': True,
# }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# ------------- THEMES -----------------------------------
# Sphinx themes store :https://sphinx-themes.org/
# html_theme = 'alabaster' # << default Sphinx theme
html_theme = 'sphinx_rtd_theme' # << preferred Sphinx theme
# html_theme = 'sphinx_book_theme' # << content shifted !!!

# ------------------ FAVICON ---------------------
html_favicon = '_static/favicon.ico'

#---------------------STATIC----------------------
html_static_path = ['_static']

#---------------------CUSTOM CSS----------------------
html_css_files = ['css/customWidth.css']

#---------------------CUSTOM JS----------------------
#html_js_files = ['some_js_file.js']

# --------------------- expanded/collapsed web element  ----------
# Add custom CSS file to the list of files to include in the HTML output


# def setup(app):
#     """
#     Method for managing of document sections.
#     To make it as expanded/collapsed web element
#     """
#     app.add_css_file("css/customExpanCollapseSection.css")
#     app.add_js_file("js/customExpanCollapseSection.js")
