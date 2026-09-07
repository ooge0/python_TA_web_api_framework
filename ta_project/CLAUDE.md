# CLAUDE.md

My notes on how this framework is built, where it stands, and what I am changing
next. For the ranked backlog see `improvements.md`; for the milestone order see
`ROADMAP.md`.

## 1. What this is

My test-automation framework for the *restful-booker* practice application:

- UI + front-end API: `https://automationintesting.online`
- back-end API: `https://restful-booker.herokuapp.com`

I built it to practise assembling, documenting and publishing a framework end to
end and to sample a wide modern tooling stack (see
`docs/source/about/about_this_guide.rst`). It is a learning and portfolio
project, not a production suite.

Originally active Sep–Dec 2024 (33 commits, single author, Windows-primary).
This copy is the working tree for the `ROADMAP.md` milestones; see
`## 10. Where M1–M8 landed` for what has changed since the review.

## 2. Layout and how the pieces connect

```
core/
  api/         APIClient (requests.Session wrapper) + endpoint registries
    services/  per-resource service objects: AuthApi / BookingApi / RoomApi /
               BrandingApi / MessageApi / ReportApi / PlatformBookingApi
  pages/       Selenium page objects: BaseFrontPage -> Home / LoginAdmin / AdminRooms
  locators/    (By, "selector") tuple locator classes, one per page
  data/
    data_models/    pydantic v2 models with from_dict / to_dict shims
    json_schemas/   plain-dict JSON Schemas for /booking
config/        config.ini (configparser), settings.py (typed + cached),
               logger_config.py (loguru), pylint.rc
utilities/     api_utils, excel_data_provider, general_utils, read_configurations;
               _devtools/ holds the doc-generation scripts
resources/test_data/  fixtures_api_test_data.py, MIME catalogue, booker_test_data.xlsx
tests/
  conftest.py            the only project conftest; composes fixtures via pytest_plugins
  api_tests/             requests-based; business_core/ (auth, booking, resources) + other/ (schema, perf)
  web_app_tests/         Selenium; test_login_page/ + tests_home_page/ + test_sut_drift_episode.py
docs/          large Sphinx site (source/); build output is git-ignored
.github/workflows/  ci.yml (lint + test + coverage), deploy-docs.yml
tasks.py       invoke tasks — docs + UML build only
pyproject.toml root pytest config (markers, testpaths, addopts)
tox.ini        py312 / lint / test(+allure) / pdf docs / html docs
```

How I wired the moving parts — know this before editing:

1. **API calls** go through a **per-resource service object**
   (`core/api/services/`) that binds an endpoint, an `APIClient` and the pydantic
   models. `APIClient._request()` is still the single dispatcher underneath
   (logging + secret redaction + `timeout` + `raise_for_status()`), with thin
   `get/post/put/patch/delete` wrappers. Endpoint strings live in `BackEndPoints`
   / `FrontEndPoints`. Negative tests that need a raw call use `service.client`.
2. **Locators are `(By.X, "selector")` tuples** in per-page classes
   (`core/locators/`). `BaseFrontPage` (`core/pages/base_page.py`) takes those
   tuples directly: `find / find_all / click / type / text_of / attr_of /
   is_visible`.
3. **Waits are explicit only** — `WebDriverWait`, no `time.sleep`, no implicit
   wait. `DEFAULT_WAIT = 15`, `SHORT_WAIT = 4` on `BaseFrontPage`.
4. **Models** are pydantic v2 (`core/data/data_models/`) with `from_dict` /
   `to_dict` compatibility shims; `/booking` responses are also JSON-Schema
   validated.
5. **Config** is read once into a cached, typed `Settings` object
   (`config/settings.py`, `get_settings()`); import that, do not call
   `read_configuration` directly. Credentials come from `config.ini
   [credentials]` (public demo creds, not secrets).
6. **Test data** is inline constants + `Faker` for most cases. One data-driven
   case: `ExcelDataProvider` reads the invalid-login rows from
   `booker_test_data.xlsx` into a `parametrize` on the front-end auth negative
   test.
7. **Fixtures** are composed in `tests/conftest.py` via `pytest_plugins` from
   `core/api/api_client_fixtures.py` (clients + service objects),
   `resources/test_data/fixtures_api_test_data.py` and the two
   `fixtures_for_*_tests.py` files.
8. **Reporting**: Allure decorators, screenshot-on-failure attached to Allure via
   the `log_failure_by_picture` fixture + `pytest_runtest_makereport` hook,
   loguru file/console logging, per-test start/outcome logging via an autouse
   fixture. `pytest-check` for soft assertions in the multi-field checks.

## 3. Running things

```bash
pytest                     # root pyproject.toml is picked up automatically
pytest -n auto             # parallel (pytest-xdist) - the default in tox / CI
pytest -m api              # or -m ui; markers are auto-applied by path
pytest --cov               # coverage (also runs in CI)

tox -c tox.ini             # py312 + lint + docs + allure test env
python -m invoke build-html   # Sphinx HTML into docs/_build/html
```

The suite hits **live shared public services**. It is network-dependent, but
every write test now **creates and deletes its own record** (no hard-coded
ids), so it is deterministic and safe under `-n auto`. The Selenium layer runs
against today's SPA (rebuilt in M8).

## 4. Feature inventory (what exists)

**API testing** (48 tests)
- Per-resource service objects over one `APIClient` (`requests.Session`,
  all five verbs, central dispatch with secret-redacting logging, `timeout`,
  `raise_for_status`).
- Back-end: auth (`POST /auth`, negative matrix, Hypothesis fuzz, ~70-entry MIME
  matrix), `/booking` CRUD incl. no-token 403 / missing-id 404 / malformed 500,
  `/ping`, JSON-Schema validation, single-request latency checks.
- Front-end (platform, `/api`): auth (login / validate / logout, incl.
  data-driven invalid rows from Excel), `/room` get+create+delete, public
  reservation + overlap 409, room bookings, branding, message inbox, report.
- Front-end API is fully covered (15/15 requirements); back-end is one Low case
  short (`?firstname=` filter).

**UI testing** (13 tests, Selenium, re-targeted at the SPA in M8)
- Page objects `HomeFrontPage` / `LoginAdminPage` / `AdminRoomsFrontPage` over
  `BaseFrontPage`; `(By, "selector")` tuple locators; explicit waits only.
- Home: footer, nav brand, contact form (valid + empty), "Book now" links.
- Admin: login (valid / invalid / placeholders), navbar, logout, rooms table.
- Browser factory fixture: chrome / firefox / edge, headless toggle, driver on
  the test class, quit on teardown; waits for the async render.
- One skipped test (`test_sut_drift_episode.py`) as a standing reminder of the
  SUT-drift episode.

**Data**
- pydantic v2 models with `from_dict` / `to_dict` shims; nested booking model.
- `Faker` for contact / booking / reservation details.
- One data-driven example: `ExcelDataProvider` (openpyxl) reads the invalid
  rows from `booker_test_data.xlsx`.

**Test infrastructure**
- Single conftest with plugin composition, autouse logging, screenshot-on-fail,
  `pytest_runtest_makereport` report attribute hook.
- Parametrisation via `parametrize` (incl. `indirect`), Excel, Faker, Hypothesis.
- PyHamcrest matchers as the main assertion style; `pytest-check` for the
  multi-field soft assertions.
- Markers (`api` / `ui` / ...) auto-applied by path; `pytest -n auto` by default.

**Orchestration / tooling**
- CI: `.github/workflows/ci.yml` - pylint (reported) + `pytest -n auto -m "not
  ui"` with coverage on every push / PR.
- `tox`: `py312`, `lint`, `test` (+Allure), `make_pdf_docs`, `make_html_docs`.
- `invoke` tasks for Sphinx HTML/PDF build and pyreverse UML.
- `pip-tools`: `requirements.in` -> compiled `requirements.txt`.

**Documentation**
- Sphinx site: autodoc + autosummary + AutoAPI, `rst2pdf`, RTD theme; build
  output is git-ignored, published from CI.
- Guide pages (`about/`, `config/`), a glossary, pyreverse UML, and the QA &
  Testing section (`docs/source/qa/`).
- Large embedded README that doubles as a personal pytest / Sphinx manual.

**QA / QC artifacts** (built in M4, under `docs/source/qa/`)
- Test plan; feature / requirements catalogue with stable IDs
  (`FEAT-*` / `REQ-*` / `TC-*`); test cases mapped to requirements (plus
  placeholders for the gaps); requirements traceability matrix;
  coverage-by-feature table; `what_my_tests_cover` summary; an episode log.
- `pytest-cov` wired (no enforced floor yet).
- Still open: normalise the Allure taxonomy (item 68); a CI catalogue-vs-matrix
  diff (item 63); a formal known-issues log (item 67).

## 5. What is still missing

Most of the original gap list was closed in M1–M8 (see §10). What remains:

**Coverage**
- Back-end `GET /booking?firstname=` filter — the one Low requirement with no
  test.
- Home-page room listing / room details / the reservation calendar — no UI
  tests (out of M8 scope; would be a new milestone).
- No load testing, contract testing, visual or accessibility testing.

**Isolation / infra**
- Still runs against the live shared public services — no local stub, no
  ephemeral environment, no rerun/flake handling.
- No Docker / devcontainer / Selenium Grid / remote WebDriver; drivers assumed
  on PATH.

**QA / QC artifacts**
- `pytest-cov` runs but there is no enforced floor yet.
- The Allure `epic/feature/story` taxonomy is still not normalised
  (`improvements.md` item 68); the CI does not yet diff the traceability matrix
  against the catalogue (item 63).
- No formal defect / known-issues log — the episode log
  (`docs/source/qa/episodes.rst`) and `improvements.md` carry that for now.

## 6. My approach on this project

From how I built it, the `about/` guide, and the commit history:

1. **Self-education and portfolio first.** My stated goals: grow my skills,
   produce a guide "better than I found on different platforms", "teaching is
   learning twice". The framework is the vehicle for learning the tools.
2. **Breadth-first tool sampling.** I wired in a wide stack — pytest, xdist,
   Allure, Hypothesis, PyHamcrest, Faker, jsonschema, openpyxl, SQLite, loguru,
   tox, pip-tools, invoke, Sphinx + AutoAPI, pyreverse/PlantUML, tach,
   pydocstyle. Most I exercised once to show the pattern rather than used
   throughout.
3. **Structure and documentation up front.** Layered package tree from the
   start, module/class/method docstrings almost everywhere, type hints on nearly
   every signature, a Sphinx site generated from them.
4. **Data-driven testing as a theme.** I wanted to demonstrate the technique;
   after M5 it survives as one honest example (Excel invalid-login rows feeding
   the front-end auth negative test) rather than three parallel unused sources.
5. **Documentation as a deliverable in its own right.** The README and Sphinx
   guide are teaching material and my own reference (full pytest and
   Sphinx-from-scratch tutorials embedded), not repo onboarding.
6. **One intense burst, then a pause.** A lot of the later effort went into
   fighting the docs-publishing pipeline (many "Edited deploy_docs.yml", "again
   same result" commits); I settled it by committing the built HTML and pushing
   `gh-pages` by hand.
7. **Solo, with no feedback loop.** No PRs, no review, no CI gate — so
   copy-paste drift, the uncollected test class and the no-op assertions never
   got caught. My breadth ran ahead of my verification.

## 7. Where the project stands

At the review the architecture was ahead of the execution: the layering, the
`APIClient` dispatcher, the fixture composition and the toolchain were the shape
I wanted, but the verification discipline had not caught up — untested code
paths, a whole UI class that did not collect, no-op assertions, no CI.

M1–M8 closed that gap (see §10). The suite now collects cleanly, runs green
(48 API + 13 UI, 1 skipped), runs under CI with coverage, and the test design
is written down under `docs/source/qa/`. The remaining work is coverage breadth
and the isolation-from-live-services problem, not correctness of what exists.

## 8. QA / QC artifacts — the reference I built them from

Built in M4 under `docs/source/qa/` (test plan, feature / requirements
catalogue, test cases, traceability matrix, coverage-by-feature, episode log).
The references below are what I used and would extend them with.

1. **SUT feature / requirements catalogue** — one table with stable IDs
   (`REQ-AUTH-01`, `REQ-BOOK-03`, …) for restful-booker: auth (`/auth`,
   `/auth/login`, `/auth/logout`), booking CRUD (`/booking`), rooms (`/room`),
   health (`/ping`), and the UI pages (home, contact form, admin login, admin
   rooms, report, messages, branding, logout). Source of truth for the rest.
   Refs: restful-booker API docs
   <https://restful-booker.herokuapp.com/apidoc/index.html>; ISTQB Foundation
   syllabus, "Test design techniques" <https://www.istqb.org/>;
   ISO/IEC/IEEE 29119-3 test documentation templates
   <https://softwaretestingstandard.org/>.

2. **Test-case specification, organised by feature** — per case: ID, linked
   `REQ-*`, title, type (functional / negative / schema / performance),
   priority, preconditions, steps, expected result, automation status, pytest
   node ID. Keep it next to the feature it covers: Markdown/CSV/YAML in
   `docs/qa/test-cases/` (one file per feature), or a TMS (Qase, TestRail,
   Zephyr, Xray, Testmo) with each automated test linked back via
   `@allure.testcase("QASE-123", url=...)` / `allure.dynamic.label("testcase", ...)`.
   Refs: Allure test-case & link decorators
   <https://allurereport.org/docs/pytest-reference/>; pytest markers as a
   case-type taxonomy <https://docs.pytest.org/en/stable/how-to/mark.html>;
   Ministry of Testing, writing test cases <https://www.ministryoftesting.com/>.

3. **Requirements Traceability Matrix (RTM)** — columns:
   `requirement ID | feature | test case ID | pytest node ID | type | priority |
   last result | gap?`. One row per requirement×case; shows both untested
   requirements and orphan tests. Build it manually in
   `docs/qa/traceability-matrix.csv`, or semi-automate: tag tests
   (`@allure.label("requirement", "REQ-BOOK-01")` or `@pytest.mark.req(...)`),
   export with `pytest --collect-only -q` + a small script (reuse
   `utilities/_devtools/make_list_of_tests.py` as the seed), and diff against
   the catalogue in CI.
   Refs: ISTQB glossary, "traceability matrix" <https://glossary.istqb.org/>;
   ISO/IEC/IEEE 29119-3 §"Traceability"; Ministry of Testing, "How to create a
   requirements traceability matrix" <https://www.ministryoftesting.com/>.

4. **Coverage matrix by feature** — `feature | planned cases | automated |
   passing | known gaps`. Fill automated/passing from the last Allure /
   `pytest-json-report` run; fill planned/gaps from the catalogue.
   Refs: `pytest-json-report` <https://pypi.org/project/pytest-json-report/>;
   `allure-pytest` results model <https://allurereport.org/docs/pytest/>.

5. **Code-coverage measurement** — add `pytest-cov`, set a floor, publish the
   report. It measures *code* exercised, not *requirements* covered — I still
   need matrices 3 and 4.
   Refs: `pytest-cov` <https://pytest-cov.readthedocs.io/>; `coverage.py`
   <https://coverage.readthedocs.io/>.

6. **Test plan** — one short page: objective, in/out of scope, test levels &
   types, environments (the two public services + browsers), data strategy
   (constants / Faker / one Excel case), entry & exit criteria, risks (shared
   live services, xdist races), reporting (Allure).
   Refs: ISO/IEC/IEEE 29119-3 test-plan template; IEEE 829-2008 (historic).

7. **Defect / known-issues log** — `docs/qa/known-issues.md`: ID, area,
   severity, description, linked test (xfail/skip), status. Move the triaged
   `improvements.md` blockers/bugs here; link each `@pytest.mark.xfail(
   reason=..., strict=True)` back to its entry.
   Refs: pytest skip/xfail
   <https://docs.pytest.org/en/stable/how-to/skipping.html>.

8. **Normalise the Allure taxonomy first** — settle one
   `epic → feature → story` vocabulary keyed to the catalogue and apply it
   everywhere, so Allure's Behaviors view becomes a usable secondary coverage
   lens.
   Refs: Allure behaviours / labels <https://allurereport.org/docs/pytest/>.

Optional: `pytest-bdd` (<https://pytest-bdd.readthedocs.io/>) would keep the
feature catalogue and the test cases in one place as Gherkin `.feature` files,
if I decide I want living feature-oriented specs.

## 9. Reminders when I work here

- Config is `pyproject.toml` at the root; `pytest` picks it up with no `-c`.
- Call `get_settings()` (cached), not `read_configuration` directly.
- API tests go through the service objects in `core/api/services/`; use
  `service.client` only for the deliberate raw / negative calls.
- Locators are `(By.X, "selector")` tuples — no enum name-suffix dispatch any
  more.
- Editing a model's `to_dict` affects live POST bodies — check callers.
- The suite needs network and the two public services to be up.
- The Selenium layer targets the **current** SPA; if `automationintesting.online`
  changes again, re-capture locators (episode 1 in `qa/episodes.rst`).

## 10. Where M1–M8 landed

- **M1** made the suite honest: every test collects; no assertion that cannot
  fail; the front-end API drift fixed (`/api` prefix, token in body, 401).
- **M2** put it under CI (`.github/workflows/ci.yml`): pylint + `pytest -n auto`
  + coverage on every push / PR.
- **M3** made runs repeatable: per-client `Session`, request `timeout`, secrets
  redacted in logs, credentials single-sourced to `config.ini [credentials]`,
  every write test creates + cleans up its own record.
- **M4** wrote the test-design layer under `docs/source/qa/` (test plan,
  feature / requirements catalogue with IDs, test cases, traceability matrix,
  coverage-by-feature) and merged the Sphinx sections.
- **M5** cleaned the core: pydantic models, typed cached `Settings`,
  per-resource service objects, `(By, "selector")` locators, `utilities/` split
  (`_devtools/`), the dead Excel-factory / SQLite / reference-data apparatus
  removed (one Excel data-driven example kept), `pytest-check` soft assertions.
- **M6** finished the edges: naming / encodings, README quickstart, docs cruft
  removed, `tasks.py` / `setup_env.bat` fixed, docstring pass. Sphinx builds
  with 0 errors.
- **M7** filled the API coverage gaps: back-end +10, front-end +9; front-end API
  fully covered.
- **M8** re-targeted the Selenium layer at the current React SPA: new tuple
  locators, rewritten `BaseFrontPage` and page objects, a render-aware
  `setup_and_teardown`. 13 UI tests pass.
