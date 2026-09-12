# Python test automation framework

Portfolio project demonstrating automated tests for the [restful-booker](https://automationintesting.online) practice application, implemented with two independent automation stacks.

## Project layout

| Folder | Stack | Status |
|---|---|---|
| [playwright_v3/](playwright_v3/README.md) | Python · Playwright · pytest | Active |
| [selenium_v2/](selenium_v2/README.md) | Python · Selenium · pytest | Legacy reference |

SUT (front-end): <https://automationintesting.online>  
SUT (back-end API): <https://restful-booker.herokuapp.com>

---

## Quick start — playwright_v3

```bash
cd playwright_v3
pip install -r requirements.txt
playwright install chromium firefox --with-deps
pytest tests/ --browser chromium -n0 -q
```

See [playwright_v3/README.md](playwright_v3/README.md) for full setup instructions, test categories, and CI badge.

## Quick start — selenium_v2

```bash
cd selenium_v2
pip install -r requirements.txt
pytest tests/ -c config/pytest.ini -q
```

See [selenium_v2/README.md](selenium_v2/README.md) for the original Selenium v2 framework documentation.
