ADR-005: Tuple locators over enum-name parsing
================================================

**Status:** Superseded by :ref:`adr_012` (v3 uses plain CSS/XPath strings with Playwright's ``page.locator()``)

**Context.** The original ``BasePage.find_element_by_locator`` parsed enum
member names (``..._XPATH_LOCATOR`` → ``By.XPATH``,
``..._CSS_LOCATOR`` → ``By.CSS_SELECTOR``).  A locator that was not named
with the right suffix would silently fail to resolve, and the naming discipline
had already been broken in several places.

**Decision.** I switched to ``(By, "selector")`` tuples stored as class
attributes in locator files.  ``BaseFrontPage.find()`` and
``BaseFrontPage.find_all()`` accept these tuples directly.

**Consequences.** The locator strategy is explicit — there is no naming
convention to maintain.  Locators are standard Selenium ``(By, value)`` pairs,
familiar to any Selenium user.  The old enum-based locator classes are no
longer used.
