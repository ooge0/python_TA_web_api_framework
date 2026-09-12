# Test plan — selenium v2 (legacy reference)

> **Status: frozen.** This framework is a legacy reference snapshot.
> Active development moved to `playwright_v3/`. No new tests will be added here.
> This plan documents the state as of December 2024.

## Objective

Verify auth, booking, and basic UI behaviour of the *restful-booker* practice
application using Python + Selenium + pytest + requests.

## Scope

| Level | In scope | Out of scope |
|---|---|---|
| API | Back-end auth, booking CRUD, schema validation, single-request latency | Front-end room/report/message/branding APIs |
| UI | Home page footer, admin login (positive only) | Admin rooms, report, messages, branding, logout verification |
| Data | Inline constants, Excel (`booker_test_data.xlsx`), SQLite seed, Faker | Environment-based data strategy |

## Test types

Functional (positive/negative), JSON-schema validation, property-based (Hypothesis),
single-request response-time checks, data-driven via Excel and SQLite.

## Known issues in this version

| ID | Area | Description |
|---|---|---|
| v2-KI-01 | BE Bookings | Hard-coded booking ids 2 and 3 — tests fail if those records don't exist |
| v2-KI-02 | BE Bookings | `test_backend_api_booking_` name collision — duplicate method names, Python discards the first |
| v2-KI-03 | BE Bookings | `assert_that(x, 200)` — int is not a matcher; assertion is a no-op |
| v2-KI-04 | UI Login | `UiTestLoginActionFlow` class silently not collected — all negative login cases lost |
| v2-KI-05 | UI Rooms | `TestLoginPage.test_ui_*` — generic names, methods likely broken |
| v2-KI-06 | FE Bookings | `test_front_api_create_booking_with_valid_token` — fixture or conftest issue |
| v2-KI-07 | All | No CI: no gate forces any of the above to surface |
| v2-KI-08 | All | Credentials logged in cleartext at INFO level |

## Environments

- Back-end API: `https://restful-booker.herokuapp.com` (shared public)
- Front-end UI: `https://automationintesting.online` (shared public)
- Browser: Chrome / Firefox / Edge (driver on PATH, headless toggle in config)
- Python 3.12; selenium 4.x

## Running the suite

```bash
cd selenium_v2
pip install -r requirements.txt
pytest -c config/pytest.ini -q
```

Driver must be on PATH. The suite hits live shared services — no cleanup,
no isolation, race conditions exist under `-n`.

## Coverage summary (as of freeze)

See `docs/qa/rtm.csv` for the full test inventory.

| Area | Automated (working) | Broken | Not collected | Gap |
|---|---|---|---|---|
| BE Authentication | 7 | 0 | 0 | 0 |
| BE Bookings | 7 | 2 | 0 | 3 |
| BE Schema | 2 | 0 | 0 | 0 |
| BE Performance | 6 | 0 | 0 | 0 |
| FE Authentication | 4 | 0 | 0 | 0 |
| FE Bookings | 0 | 1 | 0 | 2 |
| FE Other | 0 | 0 | 0 | 4 |
| UI Home page | 3 | 1 | 0 | 1 |
| UI Admin login | 0 | 0 | many | 0 |
| UI Admin (other) | 0 | 5 | 0 | 5 |
| **Total** | **29** | **9** | **~10** | **15+** | |

## Relationship to v3

`playwright_v3/` addresses every gap in this table and additionally adds:
browser-security tests, traceability markers (`REQ-*` / `TC-*`), a CI pipeline,
ruff lint, coverage measurement, and xfail-documented SUT drift cases.
