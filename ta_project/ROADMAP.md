# ROADMAP.md

Where I take this framework next. Every item number below points at an entry in
`improvements.md`. Milestones are ordered — each one makes the next easier.
This is a growth track, not a deadline.

## Why this order

The framework's shape is sound; the execution and the process around it are not.
So: first make the suite tell the truth (M1), then put something in front of it
that keeps it honest (M2), then make its results mean something (M3). Only then
is it worth investing in QA artifacts (M4) and a cleaner core (M5), finishing
with the cosmetic debt (M6) and new coverage the artifacts will expose (M7).

## Progress

| milestone | state |
|---|---|
| M1 make the suite honest | **done.** API side 23/6 -> 30/0; the static UI code bugs (items 1, 7, 8, 9, 19, 21) fixed. The UI layer targeted a version of the SPA that no longer existed - re-targeted in **M8**. |
| M2 put it under CI | **done.** `.github/workflows/ci.yml` runs `pylint` (reported) and `pytest -n auto -m "not ui"` with coverage on every push / PR; `deploy-docs.yml` builds from `docs/source`. Items 2, 3, 45, 48, 57, 59, 65 done. Coverage floor (`fail_under`) set in **M9**. |
| M3 make runs repeatable | **done.** items 15, 26, 27, 28, 29, 30, 33, 34: per-client `Session` + `default_factory`, request `timeout`, secrets redacted in logs, `read_configuration` parsed once + cached + no longer swallows errors, per-test data ownership (create + clean up), credentials single-sourced to `config.ini [credentials]`. `pytest -n auto` is the default. (The per-worker SQLite fixture landed here and was then deleted in M5 - nothing used it after M8.) |
| M4 QA artifacts | **done.** `docs/source/qa/` = test plan, feature/requirements catalogue, test cases (`TC-*`, every test mapped + placeholders), traceability matrix, coverage-by-feature, `what_my_tests_cover`, an episode log, and a known-issues log (M9). Sphinx restructured into one **QA & Testing** section, builds with **0 errors**. Items 61, 62, 64, 66 done here; 65 (cov floor) + 68 (Allure taxonomy) + 67 (known-issues) done in **M9**; 63 (CI matrix diff) is the one open item. |
| M7 expand coverage | **API done - both APIs fully covered.** Back-end 17/17, front-end 15/15 (the `?firstname=` filter closed in **M9**). Back-end +10 (negative-auth 403, missing-id 404, malformed 500, `/ping`); front-end +9 (`/api/room` CRUD, public reservation + overlap 409, room bookings, message inbox, token validate, logout, report). The remaining gaps are all UI (see M9 / KI-12). |
| M5 clean the core | **done.** 39 (pydantic models), 42 (typed cached `config/settings.py`), 40 (`core/api/services/` - `AuthApi` / `BookingApi` / `RoomApi` / `BrandingApi` / `MessageApi` / `ReportApi` / `PlatformBookingApi`; **every** API test module now calls through them - `test_api_performance.py` and `test_api_json_schema_validation.py` migrated, the last raw-client calls in the front booking flow gone), 41 (locator tuples, delivered in M8), 36 (Excel: `excel_utils.py` + `DataFactory` + `LoginCredentials` deleted, `ExcelDataProvider` kept and wired into one real data-driven test), 37 (SQLite apparatus - `db_utils`, `test_data_utils`, `core/reference_data/`, the `_isolated_db` / `validation_data` / `setup_database` fixtures - all deleted, nothing used them after M8), 38 (`utilities/_devtools/` for the doc scripts; `back_api_utils.py` / `get_names_of_tests.py` / the disabled `fix_path_*` file removed), 43/44 (dead code, `config/db_config.py`, dead fixtures), 46 (`pytest-check` soft assertions in the multi-field checks), 47 (test flag gone with `LoginCredentials`), 51 (logger path), 52 (rename). `pytest-lazy-fixture` + `regex` dropped from the deps. |
| M6 finish the edges | **done.** 10 (`BackApiAuthPayload.to_dict` returns a dict; the model is now used by the back-auth test), 22 (`HeaderModel` deleted), 23/31/32 (base-page waits, delivered in M8), 24 (`navbar1` typo), 49 (`docs/requirements.txt` constrained by the lock file), 50 (dropped unconfigured `tach`; contributor guide rewritten to the real tooling), 52/53 (naming + a docstring pass over conftest / fixtures / the migrated tests), 54 (README quickstart), 55 (deleted `index_old.rst_`, `favicon1.ico`, stale `list_of_all_project_tests*`, `facepalm.jpg`, placeholders; fixed broken includes), 56 (`pylint.rc` -> UTF-8, `project_tree.txt`), 58 (`conf.py` author, dead `templates_path`), 60 (`tasks.py`, `setup_env.bat`). **Sphinx builds with 0 errors** (stale autodoc entries for the deleted modules cleaned; RST title underlines in the QA docs fixed). |
| M8 re-target the UI layer | **done.** New `(By, "selector")` tuple locators (delivers item 41), a rewritten `BaseFrontPage` (`find/click/type/text_of/is_visible`, delivers items 31/32), new page objects for the SPA (`HomeFrontPage`, `LoginAdminPage`, `AdminRoomsFrontPage`), and a `setup_and_teardown` that waits for the async render instead of clicking the gone intro banner. `test_login_actions_validation.py` removed; `test_home_page.py` + `test_login_page.py` rewritten. **13 UI tests pass** against the live SPA. `base_locators.py` (Enum), `home_page_validation_data.py` and the DB-backed UI test gone. Requirement coverage 31 -> 41 of 52. |
| M9 close the QA loop | **done bar one item.** 68 (Allure `epic → feature → story` normalised to the catalogue - 3 epics, 13 features; documented in `qa/index.rst`), 67 (`qa/known_issues.rst` - SUT quirks + framework limitations), 65 (`[tool.coverage.*]` in `pyproject.toml`, `fail_under = 70`, `_devtools` omitted; CI fails below the floor), the `GET /booking?firstname=` filter test (back-end now 17/17). Requirement coverage 41 -> **42 of 52** (the last 10 are all UI). **Open: 63** - a CI step that diffs the traceability matrix against the catalogue. |

---

## M1 — Make the suite honest

**Goal:** a clean checkout collects every test, and every test either passes or
fails for a real reason.

Items: 1, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 19, 20, 21, 25.

Covers: the uncollected `UiTestLoginActionFlow` class; the `TypeError` /
`NameError` / missing-fixture blockers; the no-op `assert_that(x, 200)`
matchers; the shadowed duplicate tests; the vacuous Hypothesis test; the
mislabelled front-booking test; the `[excel]` config-case bug.

**Done when:**
- `pytest --collect-only` shows no lost class and no shadowed duplicates.
- No test contains an assertion that cannot fail.
- Each currently-failing test fails for a reason I have written down (feeds M4
  item 67).

---

## M2 — Put it under CI

**Goal:** every push runs lint + the suite + coverage on GitHub, red on
failure.

Items: 2, 3, 35, 45, 48, 57, 59, 65.

Covers: root pytest config so `pytest` works with no `-c` flag; a real
test/lint workflow; `pytest-cov`; markers so CI can run a fast subset; tox
cleanup; untracking build output and the stale test inventory so the checkout
CI sees is clean.

**Done when:**
- A GitHub Actions run installs deps, runs `pylint` on `core/` + `utilities/` +
  `tests/`, runs the suite, and uploads coverage.
- The run is red when a test fails.
- `pytest` from a fresh clone needs no `-c config/pytest.ini`.

---

## M3 — Make runs repeatable  ✅ done

**Goal:** the suite is deterministic and safe to run in parallel.

Items: 15, 26, 27, 28, 29, 30, 33, 34 (14 was folded into M1).

Done:
- one source of truth for credentials → `config.ini [credentials]`, read by the
  fixtures (item, plus `admin_page_url` corrected to `/admin`)
- per-client `requests.Session` via `default_factory`; request `timeout` (26, 27)
- secrets redacted in the API-client logs; password no longer logged on login
  (28) — a fresh log grep for `password123` / `token=<hex>` returns 0
- `read_configuration` parses once (cached) and raises on a missing
  section/key instead of returning `None` (29)
- `connect_to_db` re-raises instead of returning `None` → `TypeError` (30)
- per-worker SQLite: `db_utils` honours `TA_DB_PATH`; the `_isolated_db`
  session fixture points each `pytest -n` worker at its own tmp file; the
  committed `test_data_for_ta_framework.db` is removed (built fresh) (33)
- PUT/PATCH/DELETE booking tests create + delete their own record (34)

**Verified:**
- repeated `pytest -n auto` runs: 30 passed / 20 skipped every time
- no booking-id races
- fresh `logfile.log` has no plaintext credential or token

Decision: **`pytest -n auto` stays on** (default in `tox.ini`) - the API suite
holds up under repeated parallel runs against the shared services.

---

## M4 — Write the QA artifacts

**Goal:** `docs/qa/` holds the test-design paper trail, and the traceability
matrix is checked in CI.

Items: 61, 62, 63, 64, 66, 67, 68. Builds on the regenerated test inventory
from M2 (item 59), which becomes the feed for the traceability matrix.

Order within the milestone: 68 (fix the Allure taxonomy) → 61 (feature /
requirements catalogue) → 62 (test-case specs by feature) → 63 (RTM) → 64
(coverage matrix) → 66 (test plan) → 67 (known-issues log).

**Done when:**
- `docs/qa/` contains: `feature-catalogue.md`, `test-cases/` (one file per
  feature), `traceability-matrix.csv`, `coverage-matrix.md`, `test-plan.md`,
  `known-issues.md`.
- A CI step regenerates the test list and fails if a `REQ-*` in the catalogue
  has no linked test, or a test has no `REQ-*`.

References for each artifact are in `improvements.md` items 61–68.

---

## M5 — Clean the core

**Goal:** one way to do each thing; the design a reader would expect.

Items: 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 51.

Covers: one Excel path; one DB module; `pydantic` models; `(By.X, "selector")`
locators; a typed settings object loaded once; `utilities/` split into a real
package; dead code removed; soft assertions where a test checks several things.

**Done when:** ✅ (all met)
- No duplicated abstraction remains (Excel, DB, serialization) - one Excel
  provider, no DB layer, pydantic for serialization.
- `core/` has no module that only exists to be unused - the dead factory /
  reference-data / login-model modules are gone.
- A new API resource follows one obvious pattern: a `BaseApi` subclass in
  `core/api/services/` plus a fixture. Every API test uses that path.

---

## M6 — Finish the edges

**Goal:** the cosmetic and low-urgency debt is gone.

Items: 10, 22, 23, 24, 31, 32, 49, 50, 52, 53, 54, 55, 56, 58, 60.

Covers: consistent naming and file encodings; a real README quickstart; docs
cruft removed (`facepalm.jpg`, placeholders, `index_old.rst_`); the small
latent bugs (`HeaderModel` header name, navbar index mismatch, `to_dict`
returning a str); `tach`/`mypy` either configured or dropped; the broken
`tasks.py` / `setup_env.bat` lines.

**Done when:** ✅ (all met)
- README opens with clone → venv → `pytest`.
- The known typos / bad encodings / `tasks.py` + `setup_env.bat` lines are
  fixed; `HeaderModel` and the `to_dict`-returns-a-str bug are gone.
- Every declared dev tool is either used or removed (`tach`, `pytest-lazy-fixture`,
  `regex` dropped; `pylint` runs in CI).

---

## M7 — Expand coverage

**Goal:** close the coverage gaps the M4 catalogue makes explicit.

Not in `improvements.md` (these are new tests, not fixes). Driven by
`docs/qa/coverage-matrix.md`:

- API: `/ping`, `/auth/logout`, `/room` (front + back CRUD), front `/booking`
  via the front client, negative-auth on booking `PUT/PATCH/DELETE`,
  malformed-payload / schema-failure cases.
- UI: `AdminRoomsFrontPage` (add/list/price/amenities/delete room), Report page,
  Messages/Inbox, Logout action, Front-Page nav, home-page room listing / "Book
  this room" / room details, contact-form negative validation.

**Done when:** every `REQ-*` in the catalogue is either automated or explicitly
marked "manual" / "won't test" with a reason.

---

## M9 — Close the QA loop  ✅ done bar 63

**Goal:** finish the M4/M7 tail so the test-design layer is self-consistent and
CI-checked.

Items: 68 (Allure taxonomy), 67 (known-issues log), 65 (coverage floor), the
`GET /booking?firstname=` filter test, the stale ROADMAP rows, 63 (CI diff).

- **68** — `@allure.epic` = `Back-end API` / `Front-end API` / `Web UI`;
  `@allure.feature` = the `FEAT-*` feature in plain words; `@allure.story` only
  for an *approach* (`Negative` / `Performance` / `Schema validation`).
  Documented in `qa/index.rst`.
- **67** — `docs/source/qa/known_issues.rst`: SUT quirks the tests work around
  (logout doesn't invalidate, `/count` is the unread badge, DELETE = 201/202,
  500 on bad body) + framework limitations (live services, no retry, UI gaps).
- **65** — `[tool.coverage.run]` / `[tool.coverage.report]` in
  `pyproject.toml`; `fail_under = 70`, `_devtools` omitted; CI passes `--cov`
  (config-driven) and fails below the floor. Current: ~77%.
- **`?firstname=` filter** — `BookingApi.find(firstname=, lastname=)` +
  `test_name_filter_returns_the_matching_booking`. Back-end now 17/17.

**Done when:** ✅ (bar 63)
- Every test carries a catalogue-keyed epic + feature; the Allure Behaviors
  view is a usable coverage lens.
- `qa/known_issues.rst` exists and is wired into the QA toctree.
- CI enforces a coverage floor.
- **Open:** 63 — a CI step that tags tests with `REQ-*` and fails on an orphan
  test or an uncovered requirement.

---

## M8 — Re-target the Selenium UI layer at the current SUT

**Goal:** the UI tests run against today's `automationintesting.online` and stop
being skipped.

**Why this exists:** the framework's page objects, locators and
`setup_and_teardown` flow were written for the pre-2025 restful-booker-platform
(Bootstrap markup: `//*[@data-target='#collapseBanner']/button`,
`.hotel-room-info > .col-sm-7 > h3`, `//input[@data-testid='ContactName']`).
The site is now a client-rendered SPA and none of that markup exists, so every
UI test errors in setup (`TimeoutException` on the intro banner). The front-end
API had the same drift and was fixed in M1 (path moved to `/api`, token now in
the response body, `401` not `403`); the UI layer is the larger remaining piece.

Scope:
- Re-capture locators against the current DOM; move to `(By.X, "selector")`
  tuples while doing it (this also delivers item 41).
- Rework `BaseFrontPage` / `HomeFrontPage` / `LoginAdminPage` /
  `AdminRoomsFrontPage` for the SPA (waits for async render, no intro banner).
- Rework the `setup_and_teardown` fixture and drop `close_hacker_hover` if the
  banner is gone for good.
- Decide the admin login URL/flow (`/#/admin` vs a new route).
- Re-enable the three `web_app_tests/` modules (remove the module-level
  `pytest.mark.skip`) one at a time as they go green.
- Confirm the DB-backed UI tests still make sense; finish the SQLite per-worker
  isolation (the deferred half of M3) here.

**Done when:** `pytest -m ui` runs with no skips and every UI test passes or
xfails against a filed issue.

### Current SUT DOM (probed 2026-09-06, headless Firefox)

Home `https://automationintesting.online/` (React SPA, no intro banner):
- contact form: `#name` `#email` `#phone` `#subject` `#description`
  (also `[data-testid="ContactName|ContactEmail|ContactPhone|ContactSubject|ContactDescription"]`)
- contact submit: `//section[@id='contact']//button[normalize-space()='Submit']`
- nav: `a.nav-link` (Rooms / Booking / Amenities / Location / Contact / Admin)
- brand: `a.navbar-brand` = "Shady Meadows B&B"
- footer links (by text): "Mark Winteringham" -> `mwtestconsultancy.co.uk`,
  "Cookie-Policy" -> `/cookie`, "Privacy-Policy" -> `/privacy`,
  "Admin panel" -> `/admin`
- rooms: `section#rooms`, "Book now" -> `/reservation/{id}?checkin=..&checkout=..`

Admin login `https://automationintesting.online/admin` (note: `/admin`, not `/#/admin`):
- `#username` (placeholder "Enter username"), `#password` (placeholder "Password"),
  `#doLogin` (text "Login"), heading `h2` "Login"
- brand: `a.navbar-brand` = "Restful Booker Platform Demo"
- after login -> `/admin/rooms`; navbar links: "Rooms" (`/admin/rooms`),
  "Report" (`#reportLink`), "Branding" (`#brandingLink`),
  "Messages N" (`/admin/message`), "Front Page" (`#frontPageLink`),
  "Logout" `button`
- rooms table: `[data-testid='roomlisting']` (`#room1..#room3`), `#createRoom`,
  `#roomName`

More detail (probed 2026-09-07):
- **invalid login**: stays on the form, shows ``div.alert.alert-danger`` with
  text "Invalid credentials".
- **contact form validation**: an empty submit shows one ``#contact .alert-danger``
  div listing every error ("Subject must be between 5 and 100 characters." ...).
- **contact success**: no ``.alert-success`` - the ``#contact`` card is replaced
  with a "Thanks for getting in touch <name>! ..." block.
- **admin rooms**: ``[data-testid='roomlisting']`` rows ``#room1..``, ``#createRoom``.
- ``DELETE /api/room/{id}`` and ``DELETE /api/booking/{id}`` return **202**.

Reference-data drift to fix with this milestone: the `data_validation_admin_page_ui`
seed still says branding = "B&B Booking Management"; it is now
"Restful Booker Platform Demo". Footer hrefs are `/cookie` `/privacy` (no `#/`).

A first pass at the new ``(By, "selector")`` locators + a rewritten
``BaseFrontPage`` was drafted and reverted (the user redirected). Start from
the DOM map above.
