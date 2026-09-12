# README

Test automation framework for the restful-booker practice stack — UI,
front-end API and back-end API.

- Back-end API: <https://restful-booker.herokuapp.com>
- Front-end API + UI: <https://automationintesting.online>

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

Both live services must be reachable. The suite creates and cleans up its own
data; no manual seeding required.

## Where to find things

| Topic | Page |
|---|---|
| Framework structure and features | Overview section |
| SUT pages and endpoints | {ref}`sut_description` |
| Installation and environment | {ref}`setup_and_running` |
| How to run the tests | {ref}`running_tests` |
| Testing philosophy and approach | {ref}`qa_testing_philosophy` |
| What the tests cover | {ref}`qa_what_covered` |
| Feature catalogue and test cases | {ref}`qa_feature_catalogue`, {ref}`qa_test_cases` |
| Traceability and coverage | {ref}`qa_traceability`, {ref}`qa_coverage` |
| Allure reporting | {ref}`qa_allure_reporting` |
| Architecture decisions | {ref}`decisions_index` |
| Known issues and operational notes | {ref}`qa_known_issues`, {ref}`qa_operational_notes` |
| Sphinx docs setup | {ref}`sphinx_setup` |

## Project layout

```
core/
  api/         APIClient + per-resource service objects + endpoint registries
  pages/       Playwright page objects (BasePage → Home / LoginAdmin / AdminRooms / ...)
  locators/    CSS/XPath selector string registries
  data/        pydantic models, data factory, JSON schemas, reference data
config/        pydantic-settings Settings, logger_config (loguru)
utilities/     helpers: config, assertions, doc-graph generators, devtools
resources/     test data (Excel, SQLite, MIME catalogue), test reports
tests/
  conftest.py  fixtures, markers, screenshot-on-failure hook
  api_tests/   requests-based (back-end + front-end API)
  web_app_tests/  Playwright (home page + admin area, browser-security checks)
docs/          Sphinx source + built HTML
```

## Test suite

49 API + 24 UI tests passing, 1 skipped. 53/53 requirements covered
(traceability gate enforced in CI). Code coverage floor: 70%.
