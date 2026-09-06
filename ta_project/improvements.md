# improvements.md

My backlog for `python_TA_web_api_framework`. Severity-first. Each item is
tagged with an area: `api` `pages` `data` `config` `tests` `ci` `docs` `qa`
`repo`. For the order I plan to work through these, see `ROADMAP.md`.

Severity:
- **Blocker** — code cannot run / is silently not executed.
- **Bug** — runs, but behaviour or result is wrong.
- **Structural** — works, but design/maintainability cost.
- **Polish** — hygiene, naming, docs.
- **QA / QC artifacts** — missing test-design deliverables (severity Structural;
  grouped at the end because they are project-setup tasks with a shared
  reference list).

Line references are against commit `ccda777`. Items marked *(verify on run)* are
inferred from reading; I confirm them by running the suite once.

---

## Status

Work happens in `ta_project/` (the original tree stays frozen as the snapshot).
See `ROADMAP.md` for the milestone view.

| milestone | state |
|---|---|
| M1 make the suite honest | done for the API side (23/6 -> 30/0). UI side -> M8. |
| M2 put it under CI | done - `ci.yml` (lint + test + coverage on push/PR), `deploy-docs.yml` fixed, `pytest-cov` (43%). |
| M3 make runs repeatable | done - see the M3 block below and `ROADMAP.md`. |
| M4 QA artifacts | in progress - `docs/source/qa/` (test plan, feature catalogue, test cases, traceability matrix, coverage table) + a standalone README section. Items 61, 62, 63(doc), 64, 66 done as docs; 63(CI check), 68 remain. |
| M8 re-target the UI layer | started - SUT DOM probed & mapped into `ROADMAP.md`. |

Items done so far: 1-21, 25, 26, 27, 28, 29, 30, 33, 34, 35, 45, 48, 57, 59,
61, 62, 64, 65, 66, partial 41 / 44 / 63 (+ item 2). Remaining: 63(CI diff),
67, 68; the UI re-target (M8); M5 core cleanup; M6 polish; M7 new coverage.

**M3 - make runs repeatable (done):**
- item 26/27: `APIClient.session` -> `field(default_factory=requests.Session)`,
  request `timeout` (`DEFAULT_TIMEOUT = 30`)
- item 28: `_redact()` masks password/token/cookie/authorization in the API-client
  logs; `login_page` / `login_fixture` stop logging the password. Fresh
  `logfile.log` grep for `password123` / `token=<hex>` returns 0.
- item 29: `read_configuration` parses `config.ini` once (`lru_cache`) and raises
  `NoSectionError` / `NoOptionError` instead of swallowing them
- item 30: `connect_to_db` re-raises `sqlite3.Error`
- item 33: per-worker SQLite - `db_utils` honours `TA_DB_PATH`; `_isolated_db`
  session fixture gives each `pytest -n` worker its own tmp DB; committed
  `test_data_for_ta_framework.db` removed (always rebuilt)
- item 34: booking write tests use the shared `created_backend_booking` fixture
- credentials single-sourced to `config.ini [credentials]`; `admin_page_url`
  corrected to `/admin`
- `pytest -n auto` stays on: repeated full runs give 30 passed / 20 skipped

**M1 detail:**

| item | state | note |
|---|---|---|
| 1 | done | `UiTestLoginActionFlow` -> `TestLoginActionFlow`, `ttest_` -> `test_`; collection 38 -> 50 |
| 4 | done | front API `/api` prefix (was: false-positive `to_dict` finding) |
| 5, 6 | done | perf `NameError` / `param=` `TypeError` - module rewritten |
| 7 | done | added `branding_text_on_the_header_navbar` fixture |
| 8 | done | `home_page.py` room getters: `room_element.self.find_...` -> `room_element.find_element(By.CSS_SELECTOR, ...)` |
| 9 | done | `admin_rooms_page.py` rewritten to use the `LoginPageLocators` enum |
| 11 | done | `db_utils.create_initial_test_data` dict-unpack fixed |
| 12 | done | `read_configuration("Excel", ...)` -> `"excel"` |
| 13 | done | `assert_that(x, 200)` -> `assert_that(x, is_(200))` |
| 14 | done | perf write tests: real booking id + token (was: false-positive `password123` finding) |
| 16 | done | front-auth Hypothesis test rewritten so it actually runs |
| 17 | done | the two identical back-auth tests replaced with `missing_password` / `missing_username` |
| 18 | done | `test_front_api_create_booking_with_valid_token` -> `test_backend_api_create_booking_returns_int_bookingid` |
| 19, 21 | done | `test_home_page.py` duplicate removed; `instance_of(list)` -> `instance_of(tuple)` |
| 20 | done | shadowed duplicate `test_backend_api_booking_patch_response_is_edited_ok` removed |
| 25 | done | `get_validation_data_from_db` now raises on missing key instead of returning the input list |

Baseline API run: **23 passed / 6 failed** -> **30 passed / 0 failed**
(also stable 3x under `pytest -n auto`). Full suite: 30 passed, 20 skipped.

**Parallel runs (pulled forward from M3):** items 15, 26, 27, 34 done -
per-client `requests.Session` via `default_factory`, request `timeout`,
`get_back_end_token` no-op assert fixed, and a shared `created_backend_booking`
fixture so PUT/PATCH/DELETE booking tests create + delete their own record
instead of hard-coding id 2/3. `pytest -n auto` is the default in `tox.ini`.

**Item 2 (M2) done early:** root `pyproject.toml` now holds the pytest config
(markers, `testpaths`, `filterwarnings`); the mislocated `config/pytest.ini`
with its foreign `pythonpath` was deleted.

**Also picked up early:** item 35 (`.gitignore` `/docs/source/` bug), headless
browser default (`config.ini browser_headless_mode = 1`), partial item 41 (room
getters now use `(By.CSS_SELECTOR, ...)`).

**New milestone M8 (see ROADMAP.md):** the Selenium UI layer targets a version
of `automationintesting.online` that no longer exists - the site is now a
rewritten SPA, so all 20 UI tests error in setup on the missing intro banner.
They are skipped at module level (`pytestmark = pytest.mark.skip`, honest
reason) until M8 re-targets the locators and page objects. Item 1 (class name)
and the other static UI bugs are still fixed - the tests collect, they just
can't pass against the new markup yet.

---

## Blockers

1. `[tests]` `tests/web_app_tests/test_login_page/test_login_actions_validation.py`
   — class is `UiTestLoginActionFlow`; pytest default `python_classes = Test*`,
   so the file's ~9 tests (all my negative-login coverage, placeholder-text
   checks, constants-based login) are never collected. Method
   `ttest_ui_Login_process_validation_Admin_login_by_valid_creds` also has a
   leading-`t` typo.
   Fix: rename class to `TestLoginActionFlow`, fix `ttest_` -> `test_`.

2. `[config]` `config/pytest.ini` is not in rootdir and nothing sets `addopts` /
   `PYTEST_ADDOPTS`, so `pytest` from the repo root ignores it — markers,
   `testpaths`, `filterwarnings` are all inactive by default. It also carries a
   foreign absolute path: `pythonpath = D:/projects/Python/alex_ru/automation_qa_DemoQA`.
   Fix: move the pytest config to a root `pyproject.toml [tool.pytest.ini_options]`
   or root `pytest.ini`; delete the foreign `pythonpath`.

3. `[ci]` `.github/workflows/deploy-docs.yml` — no `actions/setup-python`, no
   `pip install` step, so `sphinx-build` is absent on the runner; build path is
   `docs` but `conf.py` lives in `docs/source/`. The workflow cannot succeed and
   there is no workflow that runs tests or lint.
   Fix: add a test/lint workflow (install `requirements.txt`, `pytest`, `pylint`);
   repair or delete the docs workflow (build from `docs/source/`, install deps).

4. `[api]` **DONE (M1).** `core/api/frontend_api_points.py` — `FrontEndPoints`
   paths (`/auth/login`, `/booking`, `/room`) return **404**: the SUT behind
   `automationintesting.online` (restful-booker-platform) serves its REST API
   under `/api`. All three front-API tests were failing.
   Fixed: prefixed the paths with `/api` (`/api/auth/login`, ...).
   *(Original item 4 - "`to_dict()` emits an `AdditionalNeeds` object" - was a
   false positive: the fixtures build the payload with `additionalneeds` as a
   plain string, so every booking POST/PUT/PATCH test passes. The field's type
   annotation is still inconsistent - folded into item 39.)*

5. `[tests]` `tests/api_tests/other/test_api_performance.py`
   `test_backend_api_booking_delete_call_response_time_check` references bare
   `ref_response_status_code` / `ref_response_time_in_seconds` (not `self.`) ->
   `NameError`.
   Fix: `self.ref_response_status_code` / `self.ref_response_time_in_seconds`.

6. `[tests]` `tests/api_tests/other/test_api_performance.py` — PATCH and DELETE
   latency tests call `backend_api_client.patch(..., param=3)` /
   `.delete(..., param=3)`. `APIClient` wrappers take `params`, not `param` ->
   `TypeError`. The `TODO !!` on lines 102 / 124 already flags the hard-coded id.
   Fix: use `params=` (or drop it) and resolve a real booking id.

7. `[tests]` `tests/web_app_tests/test_login_page/test_login_page.py`
   `test_branding_name_validation_by_shared_data_from_excel_with_path` requests a
   fixture `branding_text_on_the_header_navbar` that is defined nowhere ->
   setup error.
   Fix: add the fixture or parametrise the value like the sibling test.

8. `[pages]` `core/pages/home_page.py` `get_room_type` / `get_room_description`
   — `room_element.self.find_element_by_locator(...)`; `.self` on a `WebElement`
   -> `AttributeError`. Both methods are dead.
   Fix: `self.find_element_by_locator(...)` or `room_element.find_element(...)`.

9. `[pages]` `core/pages/admin_rooms_page.py` — builds a raw `self.locators` dict
   (duplicating `LoginPageLocators`) and calls `self.get_text("username_input_
   link_css_locator")`, passing a string where `find_element_by_locator` needs an
   Enum with `.value` / `.name` -> `AttributeError`. The class is unusable.
   Fix: use the `LoginPageLocators` Enum members like the other pages.

10. `[data]` `core/data/data_models/back_api_auth_data_models.py`
    `BackApiAuthPayload.to_dict()` returns a `str` (the token), not a dict —
    contract violation. Currently harmless (no caller), latent trap.
    Fix: return `{"token": self.token}` or rename to `token`.

11. `[data]` `utilities/db_utils.py` `create_initial_test_data` does
    `name, email, phone, ... = create_booking_details("tests")` but
    `create_booking_details` returns a **dict**; unpacking yields its keys, so
    the DB is seeded with literal strings `"name"`, `"email"`, ...
    Fix: `d = create_booking_details("tests"); name = d["name"]; ...`.

12. `[config]` `config/config.ini` section is `[excel]` but `tests/conftest.py`
    and the `excel_file_path` fixture call `read_configuration("Excel", ...)`.
    configparser section names are case-sensitive -> `NoSectionError` ->
    swallowed by `read_configuration` -> `DataFactory(None)` and the Excel
    fixtures receive `None`. *(verify on run)*
    Fix: use `"excel"`, or normalise case in `read_configuration`.

---

## Bugs

13. `[tests]` `test_back_api_booking.py:78`, `test_api_performance.py:50` —
    `assert_that(response.status_code, self.ref_response_status_code_ok, "...")`.
    The second arg is an `int`, not a `Matcher`; PyHamcrest treats it as the
    boolean form and asserts `bool(status_code)` -> always passes. The
    status-code check does nothing.
    Fix: `assert_that(response.status_code, is_(200))`.

14. `[tests]` **DONE (M1).** `tests/api_tests/other/test_api_performance.py` -
    the PUT / PATCH / DELETE booking latency tests sent only `Content-Type` and
    no auth token, so restful-booker answered **403 Forbidden**; they also
    passed `param=` (not a kwarg of `APIClient`) and one referenced undefined
    bare names.
    Fixed: rewrote the module - each write test now creates its own booking via
    a `created_booking` fixture, sends `Cookie: token=...`, targets
    `/booking/{id}`, and cleans up. `assert_that(x, 200)` no-op replaced with
    `is_(200)`.
    *(Original item 14 - "`back_api_valid_user_creds` = `password123` is wrong"
    - was a false positive: `admin` / `password123` is the correct
    restful-booker default; `admin` / `password` is correct for
    automationintesting. `test_back_api_creation_token_by_valid_creds` passes.)*

15. `[tests]` same file, `get_back_end_token` asserts `token is_not("None")` —
    the string `"None"`, not `none()`. A real `None` token passes.
    Fix: `assert_that(token, is_not(none()))`.

16. `[tests]` `test_front_api_auth.py`
    `test_front_api_creation_token_by_invalid_creds_hypothesis_check` — the inner
    `hypothesis_test()` call sits inside its own `except` block, so it never runs
    at outer scope and the test asserts nothing -> passes vacuously.

17. `[tests]` `test_back_api_auth.py` —
    `test_back_api_creation_token_by_valid_user_creds_and_no_headers` and
    `..._by_no_user_creds_and_valid_headers` have identical bodies; both do
    `user_creds = back_api_invalid_credentials` (a `(creds, headers)` tuple, not
    unpacked) then `json=user_creds`, sending a tuple as the body.

18. `[tests]` `test_front_api_booking.py`
    `test_front_api_create_booking_with_valid_token` uses `backend_api_client` +
    `back_end_api_booking_endpoint` — it does not touch the front-end booking
    endpoint. The `front_end_api_booking_endpoint` fixture is used by no test.

19. `[tests]` `tests_home_page/test_home_page.py` — `test_booking_request_valid_check`
    is defined twice; the `@pytest.mark.skip` on the first is nullified by the
    second (no skip, no assertion — just calls `create_booking_request("tests")`).

20. `[tests]` `test_back_api_booking.py` — `test_backend_api_booking_patch_response_is_edited_ok`
    is defined twice (lines ~165 and ~188); the first is shadowed. The "DELETE"
    section comment sits above a PATCH body.

21. `[tests]` `tests_home_page/test_home_page.py`
    `test_check_home_page_footer_content_old` asserts `instance_of(list)` but the
    page returns a `tuple`; the expected cookie/privacy URLs are also swapped
    versus the live site.

22. `[data]` `core/data/data_models/api_header_data_models.py`
    `HeaderModel.to_dict()` maps `user_agent` -> `"Accept"` header.
    Fix: `"User-Agent"`.

23. `[pages]` `core/locators/login_page_locators.py` vs the `self.locators` dict
    in `core/pages/admin_rooms_page.py` give different navbar `li` indices for
    REPORT/NAVBAR and FRONT_PAGE/LOGOUT (li[2] and li[3] swapped). One set is
    wrong. Consolidate to the Enum.

24. `[data]` `core/reference_data/home_page_validation_data.py` —
    `BRANDING_TEXT_ON_THE_HEADER_NAVBAR = 'branding_text_on_the_header_navbar1'`
    (trailing `1`) does not match the DB column created in `db_utils.create_tables`.

25. `[utilities]` `general_utils.py` `get_validation_data_from_db` catches
    `KeyError`, logs, then `return data` — returns the input list unchanged, so
    callers compare an assertion value against a list.

26. `[api]` `core/api/api_client.py` — `session: requests.Session = requests.Session()`
    is a dataclass field default built once at import; every `APIClient`
    (front and back) shares one `Session` and one cookie jar. `logger =
    get_logger()` is an un-annotated class attr, not a field.
    Fix: `session: requests.Session = field(default_factory=requests.Session)`.

27. `[api]` `APIClient._request` passes no `timeout` (a hang blocks the run
    forever; `config/pylint.rc` even sets `timeout-methods` for `requests`) and
    has no retry.

28. `[api]` `APIClient._request` logs full `headers=` and `json=` at INFO —
    credentials and tokens in cleartext. `login_page.py::login_to_admin_panel`
    logs the password, including on failure.

29. `[config]` `utilities/read_configurations.py` — swallows
    `NoSectionError` / `NoOptionError` and returns `None`; callers get a silent
    `None` instead of a clear failure.

30. `[utilities]` `db_utils.py` `connect_to_db` logs on error and returns `None`;
    callers do `conn, cursor = connect_to_db(...)` -> `TypeError` on unpack.

31. `[pages]` `base_page.py` `presence_of_static_element_on_the_page` hard-codes
    `By.XPATH` regardless of the locator passed in.

32. `[pages]` `base_page.py` `click()` waits for visibility, not clickability;
    `type()` does not `clear()` first.

33. `[tests]` `setup_database` fixture never drops tables and the
    `resources/test_data/test_data_for_ta_framework.db` file is committed ->
    state carries across runs.

34. `[tests]` suite runs against live shared public services with hard-coded
    booking ids 2 / 3, creates data with no cleanup, and `tox` runs `pytest -n 10`
    -> parallel mutation of the same ids -> races and flake.

35. `[repo]` `.gitignore` ignores `/docs/source/` (which is fully committed) and
    `/docs/html_docs/.doctrees/` (actual path is `docs/html/.doctrees/`), so ~78
    `.doctree` files + `environment.pickle` are tracked. Ignore rule
    `/resources/test_reports/allure_reports` also does not match the real
    `resources/test_report/`.

---

## Structural

36. `[utilities]` Two Excel abstractions — `data/data_factory` +
    `utilities/excel_data_provider.py` (class) and `utilities/excel_utils.py`
    (functions) — both reopen the workbook per call. Pick one.

37. `[utilities]` Two DB-bootstrap modules — `utilities/db_utils.py` and
    `utilities/create_database_with_mock_data.py` (older, raw SQL, `print`
    debugging, divergent schema). Delete one.

38. `[utilities]` `utilities/` is a grab-bag (13 modules: config reader,
    api/db/excel helpers, assertions with a `self` param, Faker, doc-graph
    generators). Split into a small typed package (`clients/`, `data/`,
    `_devtools/`).

39. `[data]` Every model hand-writes `from_dict`/`to_dict`. This re-implements
    what `pydantic` / `dataclasses.asdict` / `marshmallow` give for free and is
    where bugs 4 and 10 came from. Move to `pydantic` models.

40. `[api]` Endpoints are bare string-constant classes, duplicated across
    `BackEndPoints` / `FrontEndPoints`. No object binds endpoint + client +
    request/response model. Consider per-resource service objects
    (`BookingApi`, `AuthApi`).

41. `[pages]` Locator strategy is inferred from Enum member-name suffixes
    (`base_page.py::find_element_by_locator`). Correctness depends on naming
    discipline that is already broken (`HOTEL_ROOM_OPTION_SAFE__XPATH_LOCATOR`,
    XPath values containing spaces). Store `(By.X, "selector")` tuples instead.

42. `[config]` No settings object; `read_configuration` re-parses the INI on
    every call; no env / `.env` layering despite an unused `[env]` section and a
    `python-dotenv` mention in the README. Introduce a typed settings module
    (e.g. `pydantic-settings`) loaded once.

43. `[config]` `config/db_config.py` (MySQL-style `os.getenv` constants with
    placeholder defaults) is unused — the SUT DB is SQLite via `config.ini`.
    Delete it or wire it in.

44. `[repo]` Dead code: `HeaderModel`, `GeneralUtils.take_screenshot`, fixtures
    that wrap a single constant (`front_end_login_endpoint` etc.),
    `front_api_invalid_credentials_valid_headers` (both branches return the same
    tuple).

45. `[tests]` No markers are actually applied (`api` / `ui` / `smoke` /
    `regression`), so the suite cannot be sliced. Register and apply them.

46. `[tests]` No soft assertions — multi-assert tests stop at the first failure
    (e.g. `test_admin_page_content_validation_by_shared_data_from_db` has 4
    stacked `assert_that`). Use `pytest-check` or `assertpy` where appropriate.

47. `[data]` `LoginCredentials` carries a test-metadata `valid` flag on a domain
    model. Keep test intent out of the model.

48. `[ci]` `tox` `lint` env runs `pylint .\tests` only (not `core/`/`utilities/`)
    and does not pass `--rcfile=config/pylint.rc`. `-n 10` is hard-coded. Doc
    envs reinstall the full `requirements.txt` to shell out to `invoke`. The
    `test` env auto-runs a blocking `allure serve` (unusable in CI).

49. `[docs]` Doc dependencies are duplicated in `requirements.in`,
    `docs/requirements.txt`, and the intent of `.readthedocs.yaml`. Generate the
    doc set from one source.

50. `[repo]` `tach` is a declared dependency with no `tach.toml`;
    `pydocstyle` / `mypy` / `flake8` are mentioned in the contributor guide but
    unconfigured. Either configure and enforce them (pre-commit + CI) or drop
    the references.

51. `[config]` `logger_config.py` adds a file sink at import time with a
    CWD-relative path (`./resources/logger_output/logfile.log`), keeps loguru's
    default stderr sink, and has no per-test log file. Make the path absolute
    and configure in a fixture.

---

## Polish

52. `[repo]` Naming / typos: `front_api_bookingID_list_data_model.py` (not
    snake_case), `assert_that_less_then`, `get_prarmeter_value_from_db_by_table_name`,
    camelCase model fields (`roomName`, `roomPrice`),
    `project_related_data/pic/framewWork structure(31_Aug_2024).png`, README
    "bw" / "filed" / "adn".

53. `[tests]` Docstrings are copy-pasted with wrong `:param:` lists; three
    different back-auth tests share the identical "verifies that a token is not
    created ..." sentence while testing different things.

54. `[docs]` README (39 KB): generic pytest / Sphinx-from-scratch tutorials
    dominate; the run instructions are buried; `[Github repo]()` link is empty;
    the "GitHub workflow configs" section is an empty heading; paths are stale
    (`docs/build/index.html`); it lists packages that are not used
    (`webdriver-manager`, `mypy`, `python-dotenv`). Add a short
    "clone -> venv -> pytest" quickstart at the top.

55. `[docs]` `docs/source/diagrams/graphs.rst` uses `_static/images/facepalm.jpg`
    as a lead image and contains placeholders ("core.pages diagram should be
    here..."); `classes_relationships.rst` has a broken `1.. include::` line.
    Left-over files: `index_old.rst_`, `favicon1.ico`, two
    `list_of_all_project_tests*.md`.

56. `[repo]` `project_tree.txt` is a saved error string
    (`"Too many parameters - venv|build|.git"`), UTF-16. `config/pylint.rc` and
    `config/pytest.ini` are UTF-16-encoded; `pylint.rc` is the stock
    `--generate-rcfile` dump with no project tuning. Re-save as UTF-8, tune or
    delete.

57. `[repo]` Committed runtime output: `utilities/resources/logger_output/logfile.log`,
    `docs/html/` build tree (377 files incl. `.doctrees/`, `environment.pickle`,
    vendored theme assets). Add to `.gitignore` and untrack; publish docs from CI
    instead.

58. `[docs]` `docs/source/conf.py` author/copyright is `si0n4ra`; git author is
    `ooge0`. `templates_path = ['_templates']` points at a directory that does
    not exist under `docs/source/`. Reconcile attribution, fix or drop the path.

59. `[tests]` `resources/list_of_all_project_tests.md` is stale — method names
    and the "Total tests: 38" count no longer match the code. Regenerate it in
    CI or delete it.

60. `[tasks]` `tasks.py::make_uml_diagram_for_core_api_api_client` runs
    `pyreverse - o png - p ...` (spaces in the flags) — cannot work.
    `build_html_` applies two `re.sub` calls to the original string; the second
    discards the first. `setup_env.bat` line 4 has a bash-ism
    (`SET PYTHONPATH="$(pwd)"`) that does not expand on Windows.

---

## QA / QC artifacts (test-design deliverables)

Severity: Structural. Almost no test-design paper trail exists. Home: a new
`docs/qa/` folder (plain Markdown / CSV so it diffs and reviews), generated from
code where possible. Sequenced as `ROADMAP.md` M4.

61. `[qa]` **No SUT feature / requirements catalogue.** Build one table with
    stable IDs (`REQ-AUTH-01`, `REQ-BOOK-03`, …) for restful-booker: auth
    (`/auth`, `/auth/login`, `/auth/logout`), booking CRUD (`/booking`), rooms
    (`/room`), health (`/ping`), and UI pages (home, contact form, admin login,
    admin rooms, report, messages, branding, logout). Source of truth for
    items 62–64.
    Refs: `restful-booker` API docs
    <https://restful-booker.herokuapp.com/apidoc/index.html>; ISTQB Foundation
    syllabus <https://www.istqb.org/>; ISO/IEC/IEEE 29119-3 templates
    <https://softwaretestingstandard.org/>.

62. `[qa]` **No test-case specification, by feature.** Per case: ID, linked
    `REQ-*` ID, title, type (functional / negative / schema / performance),
    priority, preconditions, steps, expected result, automation status, pytest
    node ID. Hold it as Markdown/CSV/YAML in `docs/qa/test-cases/` (one file per
    feature) or in a TMS (Qase / TestRail / Zephyr / Xray / Testmo) with each
    automated test linked back via `@allure.testcase(...)`.
    Refs: Allure decorators
    <https://allurereport.org/docs/pytest-reference/>; pytest markers
    <https://docs.pytest.org/en/stable/how-to/mark.html>; Qase
    <https://qase.io/>; TestRail <https://www.testrail.com/>.

63. `[qa]` **No requirements traceability matrix.** Build
    `docs/qa/traceability-matrix.csv` with
    `requirement ID | feature | test case ID | pytest node ID | type |
    priority | last result | gap?`. Semi-automate: tag tests
    (`@allure.label("requirement", "REQ-BOOK-01")` or a `@pytest.mark.req(...)`),
    export via `pytest --collect-only -q` + a small script (extend
    `utilities/make_list_of_tests.py`), diff against item 61 in CI.
    Refs: ISTQB glossary "traceability matrix" <https://glossary.istqb.org/>;
    ISO/IEC/IEEE 29119-3; Ministry of Testing
    <https://www.ministryoftesting.com/>.

64. `[qa]` **No coverage matrix by feature.** `feature | planned cases |
    automated | passing | known gaps`. Fill automated/passing from the last
    Allure or `pytest-json-report` run; fill planned/gaps from item 61. Record
    the current known gaps: `/room` (front+back), `/ping`, `/auth/logout`,
    admin rooms, report, messages, logout, contact-form negative,
    negative-auth on booking `PUT/PATCH/DELETE`.
    Refs: `pytest-json-report` <https://pypi.org/project/pytest-json-report/>;
    `allure-pytest` <https://allurereport.org/docs/pytest/>.

65. `[qa]` **No code-coverage measurement.** Add `pytest-cov`, set a floor in
    CI, publish the HTML/XML report. (Measures code exercised, not requirements
    covered — items 63–64 are still needed.)
    Refs: `pytest-cov` <https://pytest-cov.readthedocs.io/>; `coverage.py`
    <https://coverage.readthedocs.io/>.

66. `[qa]` **No test plan.** One short page: objective, in/out of scope, test
    levels & types, environments (two public services + browsers), data
    strategy (constants / Excel / SQLite), entry & exit criteria, risks (shared
    live services, no cleanup, xdist races), reporting (Allure).
    Refs: ISO/IEC/IEEE 29119-3 test-plan template; IEEE 829-2008 (historic).

67. `[qa]` **No defect / known-issues log.** `docs/qa/known-issues.md`: ID,
    area, severity, description, linked test, status. Move the triaged
    Blockers/Bugs above into it; link each `@pytest.mark.xfail(reason=...,
    strict=True)` back to its entry.
    Refs: pytest skip/xfail
    <https://docs.pytest.org/en/stable/how-to/skipping.html>.

68. `[qa]` **Allure taxonomy is inconsistent** (`"back-end Auth feature"`,
    `"front-end- Booking"`, `"Booking"`, `"login_flow"`, …). Settle one
    `epic → feature → story` vocabulary keyed to item 61 and apply it across all
    tests, so the Behaviors view works as a secondary coverage lens. Do this
    before 63–64.
    Refs: Allure behaviours / labels <https://allurereport.org/docs/pytest/>.

> Optional: `pytest-bdd` (<https://pytest-bdd.readthedocs.io/>) keeps the
> feature catalogue and the test cases in one place as Gherkin `.feature`
> files, if living feature-oriented specs are the goal.
