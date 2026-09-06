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

Active Sep–Dec 2024, 33 commits, single author, Windows-primary. No packaging
(`pyproject.toml`/`setup.py` absent).

## 2. Layout and how the pieces connect

```
core/
  api/         APIClient (requests.Session wrapper) + endpoint constant registries
  pages/       Selenium page objects: BaseFrontPage -> Home / LoginAdmin / AdminRooms
  locators/    Enum locator registries (BaseLocators + per-page subclasses)
  data/
    data_models/    @dataclass models with hand-written from_dict / to_dict
    data_factory/   DataFactory -> ExcelDataProvider (openpyxl)
    json_schemas/   plain-dict JSON Schemas for /booking
  reference_data/  string-constant classes = DB column names
config/        config.ini (configparser), logger_config.py (loguru), pytest.ini, pylint.rc
utilities/     13 helper modules: config reader, api/db/excel helpers, assertions, doc-graph generators
resources/test_data/  fixtures_api_test_data.py, MIME catalogue, committed .xlsx + .db
tests/
  conftest.py            the only project conftest; composes fixtures via pytest_plugins
  api_tests/             requests-based; business_core/ (auth, booking) + other/ (schema, perf)
  web_app_tests/         Selenium; test_login_page/ + tests_home_page/
docs/          large Sphinx site (source/) + committed build output (html/)
tasks.py       invoke tasks — docs build only
tox.ini        py312 / lint / test(+allure) / pdf docs / html docs
```

How I wired the moving parts — know this before editing:

1. **API calls** go through `APIClient._request()` (`core/api/api_client.py`) —
   one dispatcher with logging + `raise_for_status()`, thin `get/post/put/patch/
   delete` wrappers. Endpoints are bare string constants in `BackEndPoints` /
   `FrontEndPoints`. Nothing binds an endpoint to a client and a model; tests
   assemble the three by hand.
2. **Locator strategy is chosen by parsing the Enum member-name suffix**
   (`core/pages/base_page.py::find_element_by_locator`): `..._XPATH_LOCATOR` ->
   `By.XPATH`, `..._CSS_LOCATOR` -> `By.CSS_SELECTOR`, etc. A locator that is not
   named this way will not resolve.
3. **Waits are explicit only** — `WebDriverWait(driver, 10)`, no `time.sleep`, no
   implicit wait. The timeout is hard-coded per method.
4. **Models** use a uniform hand-written `from_dict()` / `to_dict()`
   (`from_list` / `to_list`) contract. No pydantic yet.
5. **Test data has three interchangeable sources**, on purpose: inline
   constants, Excel (`resources/test_data/booker_test_data.xlsx`), and SQLite
   (`resources/test_data/test_data_for_ta_framework.db`, auto-created and seeded
   by the `setup_database` fixture).
6. **Fixtures** are composed in `tests/conftest.py` via `pytest_plugins` from
   `core/api/api_client_fixtures.py`,
   `resources/test_data/fixtures_api_test_data.py` and the two
   `fixtures_for_*_tests.py` files.
7. **Reporting**: Allure decorators, screenshot-on-failure attached to Allure via
   the `log_failure_by_picture` fixture + `pytest_runtest_makereport` hook,
   loguru file/console logging, per-test start/outcome logging via an autouse
   fixture.

## 3. Running things

```bash
# tests (root has NO pytest config; config/pytest.ini is NOT auto-loaded)
pytest                              # default settings, live services required
pytest -c config/pytest.ini        # to pick up markers / testpaths
pytest -n 10                        # parallel (pytest-xdist)

tox -c tox.ini                      # py312 + lint + docs + allure test env
python -m invoke build-html         # Sphinx HTML into docs/html/
```

The suite hits **live shared public services** and uses **hard-coded record
IDs** (booking 2 and 3). It is network-dependent, creates real data with no
cleanup, and races under `-n`. Fixing that is `ROADMAP.md` M3.

## 4. Feature inventory (what exists)

**API testing**
- `APIClient`: shared `requests.Session`, all five verbs, central dispatch with
  structured logging and `raise_for_status`.
- Endpoint registries for front and back APIs.
- Auth: token via `POST /auth` (cookie) / `POST /auth/login` (`Set-Cookie`),
  regex token extraction, manual `Cookie: token=` header assembly.
- JSON-Schema validation of `/booking` responses (`jsonschema`), happy-path.
- Latency assertions (`response.elapsed`), threshold 2 s.
- Property-based fuzzing of auth params (`hypothesis`).
- Content-Type negative matrix from a ~70-entry MIME catalogue.

**UI testing**
- Selenium page-object model: `BaseFrontPage` + `HomeFrontPage`,
  `LoginAdminPage`, `AdminRoomsFrontPage`.
- Enum locator registries, `__str__` -> value.
- Browser factory fixture: chrome / firefox / edge, headless toggle, driver
  attached to the test class, quit on teardown.
- Explicit waits throughout; fluent `type/click/clear` returning `self`.

**Data**
- `@dataclass` models with `from_dict`/`to_dict`; nested models for booking.
- `DataFactory` + `ExcelDataProvider` (openpyxl) with valid/invalid selection.
- `Faker` generators for contact/booking details.
- SQLite reference store: schema-as-data table definitions, idempotent seeding,
  read-as-dict / read-as-namedtuple helpers.

**Test infrastructure**
- Single conftest with plugin composition, autouse logging, screenshot-on-fail,
  `pytest_runtest_makereport` report attribute hook.
- Parametrisation via `parametrize` (incl. `indirect`), `lazy_fixture`, Excel,
  SQLite, Faker, Hypothesis.
- PyHamcrest matchers as the main assertion style.

**Orchestration / tooling**
- `tox`: `py312`, `lint` (pylint on `tests/`), `test` (+Allure, auto `allure
  serve`), `make_pdf_docs`, `make_html_docs`.
- `invoke` tasks for Sphinx HTML/PDF build and pyreverse UML.
- `pip-tools`: `requirements.in` -> compiled `requirements.txt`.
- Cross-platform bootstrap: `setup_env.bat` / `.sh`, `setup_for_tox.bat`.

**Documentation**
- Sphinx site: 12 extensions, autosummary + AutoAPI, `rst2pdf`, RTD theme.
- Hand-written guide pages (`about/`, `config/`), a substantial glossary,
  pyreverse UML + inline graphviz diagrams.
- Dual publish: ReadTheDocs + GitHub Pages (currently served from committed
  pre-built HTML).
- 39 KB README acting as a personal pytest/Sphinx manual.

**QA / QC artifacts**
- Generated test inventory: `resources/list_of_all_project_tests.md` (+ `.rst`),
  built from `pytest --collect-only` by `utilities/make_list_of_tests.py`.
  Stale.
- Allure behaviour labels (`@allure.feature`, one full `epic/story/severity`),
  inconsistent strings.
- SUT pages/endpoints described in prose in `README.md §1`.
- That is the whole set — see §5 and §8.

## 5. What is missing

**CI / process**
- No workflow that runs tests or lint. The only workflow (`deploy-docs.yml`) is
  docs-only and does not currently build. No coverage measurement, no branch
  protection, no dependency automation.
- No lint/format enforcement: black/isort/ruff absent; `mypy`, `flake8`,
  `pydocstyle`, `tach` are declared or mentioned but unconfigured.

**API coverage**
- `/ping` (health), `/auth/logout`, `/room` (front and back) — untested.
- Front `/booking` via the front client — the fixture exists, no test uses it.
- No auth-required negative tests on `PUT`/`PATCH`/`DELETE` booking.
- No malformed-payload / schema-failure tests.

**UI coverage**
- Admin Rooms management, Report page, Messages/Inbox, Logout action, Front-Page
  nav link — no tests (locators exist).
- Home-page room listing / "Book this room" / room details / reservation
  calendar — no tests (page methods exist but are broken).
- Contact-form negative validation — skipped.
- Negative login coverage is written but not collected (see `improvements.md`).

**Engineering**
- No environment layering (dev/test/prod) beyond one unused `[env]` key; no
  settings object; no `.env`/dotenv.
- No isolation from live services: no stubbed backend, no ephemeral data, no
  cleanup, no rerun/flake handling.
- No Docker / devcontainer / Selenium Grid / remote WebDriver; drivers assumed
  on PATH.
- No secrets handling: credentials are hard-coded in fixtures and `config.ini`
  and logged in cleartext.
- "Performance" tests are single-request latency asserts — no load testing;
  also no contract, visual, or accessibility testing.

**QA / QC artifacts**
- No test plan (scope, approach, environments, entry/exit criteria, risks).
- No SUT feature/requirements catalogue with stable IDs.
- No test-case specifications (ID, preconditions, steps, expected, priority,
  type) — cases live only as code.
- No requirements traceability matrix (requirement → case → automated test →
  result).
- No coverage matrix by feature; untested areas are not recorded as known gaps.
- No code-coverage measurement (`pytest-cov` / `coverage.py` not wired).
- No defect / known-issues log; bugs sit in scattered code comments.
- Allure `epic/feature/story` taxonomy is inconsistent, so it cannot stand in
  for a feature map.

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
4. **Data-driven testing as the headline theme.** My UI test docstrings
   literally narrate "here is an approach to use constants / Excel / DB as test
   data" — I wrote the tests to demonstrate the technique.
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

The architecture is further along than the execution. The layering, the
`APIClient` dispatcher, the fixture composition, the toolchain — that is the
shape I want, and it holds up:

- Correct layering (`api` / `pages` / `locators` / `data` / `config` /
  `utilities` / `tests`), centralised config and logging.
- Central `APIClient._request` with logging and `raise_for_status`.
- Explicit Selenium waits, zero `sleep`.
- Real pytest use: `pytest_plugins` composition, autouse logging, the
  `makereport` hook, screenshot-on-failure, `indirect` parametrisation,
  Hypothesis, a MIME negative matrix.
- Uniform model contract, schema validation available, Faker for data.
- A working `pip-tools` + `tox` + `invoke` + Sphinx toolchain, documented.

What has not caught up:

- Code paths I never actually ran: `room_element.self.find_element_by_locator`,
  `AdminRoomsFrontPage` passing strings into an enum-only API,
  `ApiBookingObjectPayload.to_dict()` leaving a nested object unserialised,
  `param=` kwarg to `patch`/`delete`, dict-unpacking in
  `create_initial_test_data`.
- A whole UI test class (`UiTestLoginActionFlow`) that silently does not
  collect — my negative-login coverage went with it.
- Assertions that pass without checking anything (`assert_that(x, 200)` — an int
  is not a matcher).
- Locator strategy that depends on naming discipline I have already broken.
- "catch, log, continue / return None" error handling that hides failures.
- `read_configuration` re-parses the INI on every call and swallows lookup
  errors; no settings object.
- Secrets logged at INFO; a shared mutable `Session` as a dataclass default.
- No CI, so nothing forced any of the above to surface.
- On the QC side: no test plan, no feature catalogue, no traceability matrix,
  no coverage matrix, no coverage measurement — test design lives only inside
  the test functions.

The patterns are all here; the gap is verification discipline, not knowledge.
`ROADMAP.md` is how I close it.

## 8. QA / QC artifacts — how I build the missing ones

The framework runs checks but has almost no test-design paper trail. I will add
these under a new `docs/qa/` folder (plain Markdown / CSV so it diffs and
reviews), generated from code where possible. Scheduled as `ROADMAP.md` M4.

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
   `utilities/make_list_of_tests.py` as the seed), and diff against the
   catalogue in CI.
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
   (constants / Excel / SQLite), entry & exit criteria, risks (shared live
   services, no cleanup, xdist races), reporting (Allure).
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

- `pytest` from the repo root does **not** load `config/pytest.ini`. Use
  `-c config/pytest.ini` or expect no markers / `testpaths`.
- The generated `resources/list_of_all_project_tests.md` is **stale** — names
  and counts do not match the code. Do not trust it.
- Duplicate method names exist within single test files (Python keeps the last).
- Editing a model's `to_dict` affects live POST bodies — check callers.
- The suite needs network and the two public services to be up.
