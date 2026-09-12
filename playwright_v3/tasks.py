"""
Invoke tasks - documentation build + UML generation.

Test / lint / coverage runs are driven by ``pytest`` and ``tox`` (see
``tox.ini`` and ``.github/workflows/ci.yml``), not from here.
"""
import os
import re
import shutil

from invoke import task

README_SOURCE = "README.md"
README_DEST = "docs/source/README_.md"
DOCS_SOURCE_DIR = "docs/source"
HTML_OUTPUT_DIR = "docs/_build/html"
PDF_OUTPUT_DIR = "docs/_build/pdf"
UML_OUTPUT_DIR = "docs/source/_static/diagrams/pics"


@task
def build_html(c):
    """Copy the README into the docs tree, then build the HTML site."""
    shutil.copyfile(README_SOURCE, README_DEST)
    with open(README_DEST, "r+", encoding="utf-8") as fh:
        content = fh.read()
        content = re.sub(r'<img src="', '<img src="../../', content)
        fh.seek(0)
        fh.write(content)
        fh.truncate()
    os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)
    c.run(f"sphinx-build -b html {DOCS_SOURCE_DIR} {HTML_OUTPUT_DIR}", echo=True)


@task
def clean_html(c):
    """Remove the built HTML site."""
    c.run(f"sphinx-build -M clean {DOCS_SOURCE_DIR} {HTML_OUTPUT_DIR}", echo=True)


@task
def build_pdf(c):
    """Build the PDF docs (rst2pdf)."""
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    c.run(f"sphinx-build -b pdf {DOCS_SOURCE_DIR} {PDF_OUTPUT_DIR}", echo=True)


@task
def make_uml(c, target="core"):
    """
    Generate class / package PNG diagrams for a package with pyreverse.

    Example: ``invoke make-uml --target core.api``
    """
    os.makedirs(UML_OUTPUT_DIR, exist_ok=True)
    c.run(f"pyreverse -o png -p {target.replace('.', '_')} -d {UML_OUTPUT_DIR} {target.replace('.', '/')}", echo=True)
    print(f"diagrams written to {UML_OUTPUT_DIR}")
