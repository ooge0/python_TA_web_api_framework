"""
Requirements-traceability gate (improvements.md item 63).

Cross-checks three things and exits non-zero on a mismatch:

1. every ``REQ-*`` in ``docs/source/qa/feature_catalogue.rst`` is verified by at
   least one test tagged ``@pytest.mark.req("REQ-...")`` - unless it is listed
   in ``docs/source/qa/_known_gaps.txt``;
2. every ``req`` id on a test exists in the catalogue (catches typos);
3. every collected test carries a ``req`` marker (the one skipped episode
   reminder is exempt).

Run it from the project root::

    python -m utilities._devtools.check_traceability

CI runs the same thing (``.github/workflows/ci.yml``).
"""
from __future__ import annotations

import contextlib
import io
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "docs" / "source" / "qa" / "feature_catalogue.rst"
KNOWN_GAPS = ROOT / "docs" / "source" / "qa" / "_known_gaps.txt"

REQ_RE = re.compile(r"REQ-(?:BE|FE|UI)-[A-Z]+-\d+")
# tests that legitimately have no requirement (kept visible on purpose)
EXEMPT_NODE_SUBSTRINGS = ("test_sut_drift_episode.py",)


def _read_ids(path: pathlib.Path) -> set[str]:
    if not path.exists():
        return set()
    text = "\n".join(line.split("#", 1)[0] for line in path.read_text().splitlines())
    return set(REQ_RE.findall(text))


def _collect_test_reqs() -> tuple[dict[str, set[str]], list[str]]:
    """Return ``{req_id: {nodeid, ...}}`` and the list of untagged test nodeids."""
    import pytest

    mapping: dict[str, set[str]] = {}
    untagged: list[str] = []

    class _Plugin:
        def pytest_collection_modifyitems(self, items):
            for item in items:
                marks = [m for m in item.iter_markers(name="req")]
                ids = {arg for m in marks for arg in m.args}
                if not ids:
                    if not any(s in item.nodeid for s in EXEMPT_NODE_SUBSTRINGS):
                        untagged.append(item.nodeid)
                    continue
                for rid in ids:
                    mapping.setdefault(rid, set()).add(item.nodeid)

    os.chdir(ROOT)  # module-level test data (the Excel provider) uses relative paths
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = pytest.main(
            ["--collect-only", "-qq", "-p", "no:cacheprovider", str(ROOT / "tests")],
            plugins=[_Plugin()],
        )
    if rc not in (0, 5):  # 0 = ok, 5 = no tests (shouldn't happen)
        print(buf.getvalue(), file=sys.stderr)
        print(f"pytest collection failed (exit {rc})", file=sys.stderr)
        sys.exit(2)
    return mapping, untagged


def main() -> int:
    catalogue = _read_ids(CATALOGUE)
    known_gaps = _read_ids(KNOWN_GAPS)
    tested, untagged = _collect_test_reqs()

    if not catalogue:
        print(f"no REQ-* ids found in {CATALOGUE}", file=sys.stderr)
        return 2

    uncovered = catalogue - set(tested) - known_gaps
    orphan_reqs = set(tested) - catalogue
    stale_gaps = known_gaps & set(tested)
    gaps_not_in_catalogue = known_gaps - catalogue

    problems = 0

    if uncovered:
        problems += 1
        print("FAIL - requirements with no test and not in _known_gaps.txt:")
        for rid in sorted(uncovered):
            print(f"  {rid}")

    if orphan_reqs:
        problems += 1
        print("FAIL - `req` ids on tests that are not in the catalogue (typo?):")
        for rid in sorted(orphan_reqs):
            print(f"  {rid}  <- {', '.join(sorted(tested[rid]))}")

    if untagged:
        problems += 1
        print("FAIL - collected tests with no `@pytest.mark.req(...)`:")
        for node in untagged:
            print(f"  {node}")

    if gaps_not_in_catalogue:
        problems += 1
        print("FAIL - _known_gaps.txt lists ids that are not in the catalogue:")
        for rid in sorted(gaps_not_in_catalogue):
            print(f"  {rid}")

    if stale_gaps:
        # not fatal - just means the allowlist can be trimmed
        print("note - _known_gaps.txt entries that are now covered (remove them):")
        for rid in sorted(stale_gaps):
            print(f"  {rid}")

    covered = len(catalogue) - len(uncovered) - len(known_gaps - stale_gaps)
    print()
    print(f"catalogue requirements : {len(catalogue)}")
    print(f"covered by a test      : {len(catalogue & set(tested))}")
    print(f"known gaps (allowed)   : {len(known_gaps - stale_gaps)}")
    print(f"tests carrying a req   : {sum(len(v) for v in tested.values())} tags "
          f"across {len({n for v in tested.values() for n in v})} tests")

    if problems:
        print(f"\n{problems} problem group(s) - see above.")
        return 1
    print("\nOK - every catalogue requirement is covered or a known gap; no orphan tags.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
