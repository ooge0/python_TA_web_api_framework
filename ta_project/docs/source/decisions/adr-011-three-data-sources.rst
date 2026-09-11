ADR-011: Three data sources by design
======================================

**Status:** Accepted

**Context.** Test data can come from many places: inline constants, external
files, databases, generators.  This framework is a learning and portfolio
project — demonstrating multiple approaches is part of the goal.

**Decision.** Three data sources are wired deliberately:

#. **Inline constants and Faker** — the default for most tests.
#. **Excel** — ``resources/test_data/booker_test_data.xlsx`` read by
   ``ExcelDataProvider``, feeding the front-end auth negative test.
#. **SQLite** — ``resources/test_data/test_data_for_ta_framework.db``,
   auto-created and seeded by the ``setup_database`` fixture.

**Consequences.** The framework demonstrates data-driven testing from three
independent sources, which is useful as a reference.  The trade-off:
maintaining three data paths adds complexity, and the Excel and SQLite paths
are exercised by only one test each — they exist to show the pattern, not
because the test coverage demands them.
