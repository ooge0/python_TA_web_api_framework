.. _qa_episodes:

========
Episodes
========

Things that went wrong in this framework and what I took from them. Kept here so
the mistakes stay visible instead of being quietly fixed and forgotten.

Episode 1 - the UI layer targeted a SUT that no longer exists
============================================================

**What happened.** The Selenium page objects, locators and the
``setup_and_teardown`` fixture were all written against the 2024
server-rendered ``automationintesting.online`` - Bootstrap markup, a
``//*[@data-target='#collapseBanner']/button`` intro banner,
``.hotel-room-info > .col-sm-7 > h3`` room selectors, a
``//ul[@class='navbar-nav mr-auto']/li[1]`` admin navbar. The site was rebuilt
as a React SPA. None of that markup exists now, so every UI test errors during
setup. The front-end API had drifted the same way (the path moved to ``/api``,
the token moved into the response body, ``401`` replaced ``403``).

**Why it went unnoticed.** There was no CI running the suite, and the last hands
-on session was Dec 2024. Nobody ran it against the live site after that.

**What I did.** Fixed the front-end API in M1/M7 (it is now fully covered).
Skipped the 20 UI tests at module level with a reason pointing at **M8**, kept
them collectable, and mapped the current DOM into ``ROADMAP.md``. A standing
skipped test (``tests/web_app_tests/test_sut_drift_episode.py``) keeps this
episode in every run.

**Lesson.** Run the suite in CI, on a schedule, against the live SUT. A green
suite is the definition of done - not "the code looks right".

Episode 2 - a read-only review is a guess until you run it
=======================================================

**What happened.** The first pass over the code (reading only, no execution)
produced ``improvements.md``. Two of its findings were wrong - the
``ApiBookingObjectPayload.to_dict()`` "crash" (the fixtures pass a plain string,
so it never crashed) and "``password123`` is the wrong password" (it is the
correct restful-booker default). It also missed two real bugs that only showed
up on a run - the front-end API ``/api`` path and the performance tests sending
no auth token.

**Lesson.** Mark inferred failures as *inferred* and confirm them with one run
before acting. The run is cheap; a wrong "fix" is not.

Episode 3 - a fixture that only worked in parallel
===============================================

**What happened.** The ``_isolated_db`` session fixture (per-worker SQLite)
depended on ``worker_id``, which ``pytest-xdist`` only provides when running
with ``-n``. Running plain ``pytest`` errored at setup for every test. All the
earlier verification runs happened to use ``-n auto``, so it was invisible.

**Lesson.** Do not depend on a fixture that a plugin provides conditionally.
Read ``request.config.workerinput`` directly and default sensibly. Test the
non-default path too (here: run once without ``-n``).

Episode 4 - the probe was broken, not the SUT
==========================================

**What happened.** A quick ``curl`` probe of ``POST /api/auth/logout`` returned
``400`` for every request shape, and I wrote it up as "the endpoint's contract
is unclear". The real cause: the ``python`` on ``PATH`` pointed at a missing
install, so the shell command that extracted the token produced an empty
string - every probe was logging out with no token. With a real token the
endpoint returns ``{"success": true}``.

**Lesson.** When a probe gives a surprising result, check the probe first.

Episode 5 - no CI means copy-paste drift compounds
===============================================

**What happened.** Over the life of the project several things slipped in and
stayed: two test methods with the same name in one file (Python keeps the last,
the first is silently dropped), assertions like ``assert_that(x, 200)`` where
the second argument is an int not a matcher (so it never fails), a whole UI test
class named ``UiTestLoginActionFlow`` that pytest's default ``python_classes =
Test*`` never collected.

**Lesson.** These are exactly what a linter + a CI gate catch on the first push.
They cost nothing to prevent and are tedious to find later.
