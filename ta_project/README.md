<!-- Header Section -->
<p align="left">
  <img alt="python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" width="80"/>
  <img alt="pytest" src="https://img.shields.io/badge/py-test-blue?logo=pytest" width="80"/>
  <img alt="playwright" src="https://img.shields.io/badge/-playwright-%232EAD33?style=for-the-badge&logo=playwright&logoColor=white" width="100"/>
  <img alt="requests" src="https://img.shields.io/badge/-requests-%43B02A?style=for-the-badge&logo=requests&logoColor=white" width="75"/>
</p>

[![CI](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/ci.yml/badge.svg)](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/ci.yml)
[![Docs](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/ooge0/python_TA_web_api_framework/actions/workflows/deploy-docs.yml)
![License](https://img.shields.io/badge/license-MIT-yellow)

**Test automation framework for the restful-booker practice stack — UI,
front-end API and back-end API.**

* Back-end API: [restful-booker.herokuapp.com](https://restful-booker.herokuapp.com)
* Front-end API + UI: [automationintesting.online](https://automationintesting.online)

## Quickstart

```bash
git clone <repo> && cd python_TA_web_api_framework
python -m venv .venv && .venv/Scripts/activate   # POSIX: source .venv/bin/activate
pip install -r requirements.txt
playwright install firefox chromium --with-deps   # one-time browser binary install

pytest -n auto                   # full suite in parallel (needs network + the two live SUTs)
pytest -m api                    # API tests only
pytest -m ui --browser firefox   # UI tests (Playwright, Firefox)
pytest -m ui --browser chromium  # UI tests (Playwright, Chromium)
tox -e lint                      # ruff
```

Both live services must be reachable.  The suite creates and cleans up its own
data; no manual seeding required.

## Documentation

Full documentation is built with Sphinx and published on
[ReadTheDocs](https://python-ta-web-api-framework.readthedocs.io/en/latest/index.html).
To build locally:

```bash
sphinx-build -b html docs/source docs/html
```

Key sections in the docs:

* **Overview** — framework structure, features, SUT description.
* **Setup & Running** — installation, environment, running tests, Sphinx setup.
* **QA & Testing** — testing philosophy, test inventory, test plan, feature
  catalogue, test cases, traceability matrix, coverage by feature, Allure
  reporting, other QA signals, known issues, operational notes.
* **Decisions** — architecture decision records (ADRs) for non-obvious choices.
* **Diagrams** — class and package relationships, API client wiring.
* **Reference** — auto-generated module index and glossary.

## Project layout

```
core/
  api/         APIClient + per-resource service objects + endpoint registries
  pages/       Selenium page objects (BaseFrontPage → Home / Login / AdminRooms / ...)
  locators/    (By, "selector") tuple locator registries
  data/        pydantic models, data factory, JSON schemas, reference data
config/        pydantic-settings Settings, logger_config (loguru)
utilities/     helpers: config, assertions, doc-graph generators, devtools
resources/     test data (Excel, SQLite, MIME catalogue), test reports
tests/
  conftest.py  fixtures, markers, screenshot-on-failure hook
  api_tests/   requests-based (back-end + front-end API)
  web_app_tests/  Selenium (home page + admin area)
docs/          Sphinx source + built HTML
```

## Test suite

49 API + 23 UI tests passing, 1 skipped.  53/53 requirements covered
(traceability gate enforced in CI).  Code coverage floor: 70%.

## License

MIT
