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

## M3 — Make runs repeatable

**Goal:** the suite is deterministic and safe to run in parallel.

Items: 14, 15, 26, 27, 28, 29, 30, 33, 34.

Covers: one source of truth for credentials; per-client `Session`; request
timeouts; no secrets in logs; DB rebuilt per session; no hard-coded booking
IDs — create-then-use, or an isolated data set; decide whether xdist stays on
against shared public services.

**Done when:**
- Two consecutive full runs give the same result.
- A run under `-n auto` has no ID races.
- Grepping the logs for a password or token returns nothing.

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

**Done when:**
- No duplicated abstraction remains (Excel, DB, serialization).
- `core/` has no module that only exists to be unused.
- A new page object or API resource follows one obvious pattern.

---

## M6 — Finish the edges

**Goal:** the cosmetic and low-urgency debt is gone.

Items: 10, 22, 23, 24, 31, 32, 49, 50, 52, 53, 54, 55, 56, 58, 60.

Covers: consistent naming and file encodings; a real README quickstart; docs
cruft removed (`facepalm.jpg`, placeholders, `index_old.rst_`); the small
latent bugs (`HeaderModel` header name, navbar index mismatch, `to_dict`
returning a str); `tach`/`mypy` either configured or dropped; the broken
`tasks.py` / `setup_env.bat` lines.

**Done when:**
- README opens with clone → venv → `pytest`.
- `git grep -i` for the known typos returns nothing.
- Every declared dev tool is either wired into pre-commit/CI or removed from the
  deps.

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
