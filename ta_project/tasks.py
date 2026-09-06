import os
import re
import shutil

from docutils.parsers.rst import directives
from invoke import task
from sphinx.application import Sphinx

# Define constants for file paths
README_SOURCE = "README.md"
README_DEST = "docs/source/README_.md"
DOCS_SOURCE_DIR = "docs/source/"
HTML_OUTPUT_DIR = "docs/html/"
PDF_OUTPUT_DIR = "docs/pdf_docs/"


@task
def build_html(c):
    # Run Sphinx to build HTML docs
    c.run(f'sphinx-build -b html {DOCS_SOURCE_DIR} {HTML_OUTPUT_DIR}', echo=True)


@task
def build_html_(c):
    """Run Sphinx script for building HTML docs."""
    # Copy README.md file from root dir into /docs/source and rename it as README_.md
    shutil.copyfile(README_SOURCE, README_DEST)

    # Adjust image paths by replacing [<img src="] to the  [<img src="../../] in copied README_.md file
    with open(README_DEST, 'r+', encoding='utf-8') as file:
        content = file.read()
        updated_content = re.sub(r'src="', r'src="../../', content)
        updated_content = re.sub(r'\[<img src=', r'[<img src="../../', content)
        # Replace '....' with ''
        # updated_content = re.sub(r'\]\(project_related_data/pic/', r'](../../project_related_data/pic/', updated_content)
        # updated_content = re.sub(r'\]\(../../project_related_data/pic', r'](_images/', updated_content)
        file.seek(0)
        file.write(updated_content)

    # Ensure the output directory exists
    os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

    # Run Sphinx to build HTML docs
    c.run(f'sphinx-build -b html {DOCS_SOURCE_DIR} {HTML_OUTPUT_DIR}', echo=True)


@task
def clean_html(c):
    """Run Sphinx script for building pdf docs"""
    c.run(f'sphinx-build -M clean {DOCS_SOURCE_DIR} {HTML_OUTPUT_DIR}', echo=True)


@task
def build_pdf(c):
    """Run Sphinx script for building pdf docs"""
    c.run(f'sphinx-build -b pdf {DOCS_SOURCE_DIR} {PDF_OUTPUT_DIR}', echo=True)


@task
def clean_pdf(c):
    """Run Sphinx script for clean the folder with generated docs docs"""
    c.run(f'sphinx-build -M clean {DOCS_SOURCE_DIR} {PDF_OUTPUT_DIR}', echo=True)


@task
def list_sphinx_directives(c):
    """List all available Sphinx directives."""
    # Paths to Sphinx directories
    src_dir = './docs/source'
    build_dir = './docs/build'
    doctree_dir = './docs/doctrees'
    config_dir = './docs/source'

    # Initialize a Sphinx application
    app = Sphinx(srcdir=src_dir, confdir=config_dir, outdir=build_dir, doctreedir=doctree_dir, buildername='html')

    # Print all available directives
    print("\nAvailable Sphinx directives:\n")
    for name in sorted(directives._directives):
        print(name)

@task
def make_uml_diagram_for_core_api_api_client(c):
    """Make UML diagram from .py file | make_uml_diagram_for_core_api_api_client"""
    c.run(f'pyreverse - o png - p ta_framework_ui_api  core/api/api_client.py', echo=True)


@task
def make_uml_diagram_by_pyreverse(c):
    try:
        output_directory = "project_related_data/pic/"
        print(f"Ensuring output directory exists: {output_directory}")
        os.makedirs(output_directory, exist_ok=True)

        command = (
            f'pyreverse -o png -p core_api_frontend_api_points '
            f'-d {output_directory} core/api/frontend_api_points.py'
        )
        print(f"Running command: {command}")
        c.run(command, echo=True)

        # Check for output files
        output_files = os.listdir(output_directory)
        print(f"Generated files: {output_files}")
    except Exception as e:
        print(f"Error occurred: {e}")
