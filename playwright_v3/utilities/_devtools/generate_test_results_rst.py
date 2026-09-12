"""
Test-results RST generator.

Reads ``resources/test_report/junit.xml`` (produced by pytest ``--junitxml``),
collects ``@pytest.mark.tc`` and ``@pytest.mark.req`` markers via
``pytest --collect-only``, joins the two on the test node-id, and writes
``docs/source/qa/test_results.rst``.

Run from the project root after a test run::

    python -m utilities._devtools.generate_test_results_rst

The generated file is committed alongside the source so it is always in sync
with the last run.  The CI ``docs`` job downloads the JUnit XML produced by the
``test-api`` / ``test-ui`` jobs and runs this script before ``sphinx-build``.
"""
from __future__ import annotations

import contextlib
import io
import os
import pathlib
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
_REPORT_DIR = ROOT / "resources" / "test_report"
# Prefer merged junit.xml; fall back to individual API/UI files if present
JUNIT_XML = _REPORT_DIR / "junit.xml"
_JUNIT_ALT = [
    _REPORT_DIR / "junit-api.xml",
    _REPORT_DIR / "junit_ui.xml",   # local UI run
    _REPORT_DIR / "junit-ui.xml",   # CI artifact name
]
OUT_RST = ROOT / "docs" / "source" / "qa" / "test_results.rst"
TC_CASES_RST = ROOT / "docs" / "source" / "qa" / "test_cases.rst"

# ------------------------------------------------------------------
# Data model
# ------------------------------------------------------------------

@dataclass
class TestRecord:
    nodeid: str
    tc_ids: list[str] = field(default_factory=list)
    req_ids: list[str] = field(default_factory=list)
    title: str = ""
    category: str = ""      # "Back-end API" | "Front-end API" | "Web UI"
    status: str = "no-run"  # passed | failed | error | skipped | no-run
    duration: float = 0.0
    message: str = ""


# ------------------------------------------------------------------
# Marker collection
# ------------------------------------------------------------------

def _collect_markers() -> dict[str, dict]:
    """Return ``{nodeid: {tc_ids: [...], req_ids: [...]}}``.

    Uses the same pattern as check_traceability._collect_test_reqs.
    """
    import pytest

    records: dict[str, dict] = {}

    class _Plugin:
        def pytest_collection_modifyitems(self, items):
            for item in items:
                tc_ids = [arg for m in item.iter_markers("tc") for arg in m.args]
                req_ids = [arg for m in item.iter_markers("req") for arg in m.args]
                records[item.nodeid] = {"tc_ids": tc_ids, "req_ids": req_ids}

    os.chdir(ROOT)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pytest.main(
            [
                "--collect-only", "-qq",
                "-p", "no:cacheprovider",
                # override addopts to strip --junitxml so the collect-only run
                # does not overwrite the xml written by the actual test run
                "--override-ini=addopts=-ra --strict-markers",
                str(ROOT / "tests"),
            ],
            plugins=[_Plugin()],
        )
    return records


# ------------------------------------------------------------------
# JUnit XML parsing
# ------------------------------------------------------------------

def _parse_junit(path: pathlib.Path) -> dict[str, dict]:
    """Return ``{nodeid: {status, duration, message}}``."""
    if not path.exists():
        return {}
    tree = ET.parse(path)
    results: dict[str, dict] = {}
    for tc in tree.iter("testcase"):
        classname = tc.get("classname", "")
        name = tc.get("name", "")
        # JUnit classname looks like "tests.api_tests.business_core.test_back_api_auth.TestBackApiAuth"
        # Convert to nodeid form: "tests/api.../TestClass::test_name"
        parts = classname.split(".")
        # Find the test file module (last part before class, or all if no class)
        # Try to reconstruct nodeid: path/to/file.py::Class::method
        #   classname ends in ClassName if it is a class test, else just module path
        if parts and parts[-1][0].isupper():
            class_part = parts[-1]
            module_path = "/".join(parts[:-1]) + ".py"
            nodeid = f"{module_path}::{class_part}::{name}"
        else:
            module_path = "/".join(parts) + ".py"
            nodeid = f"{module_path}::{name}"

        failure = tc.find("failure")
        error = tc.find("error")
        skipped = tc.find("skipped")
        if failure is not None:
            status = "failed"
            message = (failure.get("message") or failure.text or "")[:200]
        elif error is not None:
            status = "error"
            message = (error.get("message") or error.text or "")[:200]
        elif skipped is not None:
            status = "skipped"
            message = skipped.get("message", "")[:200]
        else:
            status = "passed"
            message = ""

        results[nodeid] = {
            "status": status,
            "duration": float(tc.get("time", 0)),
            "message": message,
        }
    return results


# ------------------------------------------------------------------
# TC-ID → title map from test_cases.rst
# ------------------------------------------------------------------

_TC_TITLE_RE = re.compile(r'"(TC-[A-Z0-9-]+)",\s*"[^"]+",\s*"([^"]+)"')

def _load_tc_titles() -> dict[str, str]:
    text = TC_CASES_RST.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in _TC_TITLE_RE.finditer(text)}


# ------------------------------------------------------------------
# Category derivation from nodeid
# ------------------------------------------------------------------

def _category(nodeid: str) -> str:
    if "api_tests" in nodeid:
        if "back_api" in nodeid or "api_json" in nodeid or "api_performance" in nodeid:
            return "Back-end API"
        return "Front-end API"
    if "web_app" in nodeid:
        return "Web UI"
    return "Other"


# ------------------------------------------------------------------
# RST helpers
# ------------------------------------------------------------------

_STATUS_SYMBOL = {
    "passed": "✓",
    "failed": "✗",
    "error": "E",
    "skipped": "S",
    "no-run": "–",
}


def _csv_table(headers: list[str], widths: list[int], rows: list[list[str]]) -> list[str]:
    lines = [
        ".. csv-table::",
        f'   :header: {", ".join(chr(34) + h + chr(34) for h in headers)}',
        f'   :widths: {", ".join(str(w) for w in widths)}',
        "",
    ]
    for row in rows:
        cells = ", ".join(f'"{str(c).replace(chr(34), chr(39))}"' for c in row)
        lines.append(f"   {cells}")
    return lines


# ------------------------------------------------------------------
# Main builder
# ------------------------------------------------------------------

def build() -> None:
    print("collecting markers …")
    markers = _collect_markers()
    print(f"  {len(markers)} tests collected")

    print("parsing JUnit XML …")
    junit: dict[str, dict] = {}
    for xml_path in [JUNIT_XML] + _JUNIT_ALT:
        if xml_path.exists():
            before = len(junit)
            junit.update(_parse_junit(xml_path))
            added = len(junit) - before
            if added:
                print(f"  {xml_path.name}: +{added} results")
    if not junit:
        print("  no junit.xml found — status will be 'no-run'")

    tc_titles = _load_tc_titles()

    # Build merged record list
    records: list[TestRecord] = []
    for nodeid, info in markers.items():
        rec = TestRecord(
            nodeid=nodeid,
            tc_ids=info["tc_ids"],
            req_ids=info["req_ids"],
            category=_category(nodeid),
        )
        if rec.tc_ids:
            rec.title = tc_titles.get(rec.tc_ids[0], "")
        # Match JUnit nodeid — try exact, then class-normalised form
        jr = junit.get(nodeid)
        if jr is None:
            # parametrised tests have "[param]" suffix in JUnit, try prefix match
            for jid, jdata in junit.items():
                if jid.startswith(nodeid.split("[")[0]):
                    jr = jdata
                    break
        if jr:
            rec.status = jr["status"]
            rec.duration = jr["duration"]
            rec.message = jr["message"]
        records.append(rec)

    # Sort: category, then status priority (failed first), then nodeid
    status_order = {"failed": 0, "error": 1, "skipped": 2, "no-run": 3, "passed": 4}
    records.sort(key=lambda r: (r.category, status_order.get(r.status, 9), r.nodeid))

    # Counts
    total = len(records)
    passed = sum(1 for r in records if r.status == "passed")
    failed = sum(1 for r in records if r.status == "failed")
    errored = sum(1 for r in records if r.status == "error")
    skipped = sum(1 for r in records if r.status == "skipped")
    no_run = sum(1 for r in records if r.status == "no-run")
    total_dur = sum(r.duration for r in records)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ------------------------------------------------------------------
    # Build RST
    # ------------------------------------------------------------------
    lines: list[str] = []

    lines += [
        ".. _qa_test_results:",
        "",
        "============",
        "Test Results",
        "============",
        "",
        f".. note:: Generated {generated_at}.  Re-run ``python -m utilities._devtools.generate_test_results_rst``",
        "   after a test run to refresh this page.",
        "",
    ]

    # Summary table
    lines += [
        "Summary",
        "=======",
        "",
    ]
    lines += _csv_table(
        ["Generated", "Total", "Passed", "Failed", "Error", "Skipped", "No-run", "Duration (s)"],
        [16, 6, 7, 7, 6, 8, 7, 12],
        [[generated_at, total, passed, failed, errored, skipped, no_run, f"{total_dur:.1f}"]],
    )
    lines.append("")

    # Per-category tables
    lines += ["By Category", "===========", ""]
    categories = ["Back-end API", "Front-end API", "Web UI", "Other"]
    for cat in categories:
        cat_records = [r for r in records if r.category == cat]
        if not cat_records:
            continue
        lines += [cat, "-" * len(cat), ""]
        rows = []
        for r in cat_records:
            tc_str = " / ".join(r.tc_ids) if r.tc_ids else "—"
            req_str = " / ".join(r.req_ids) if r.req_ids else "—"
            sym = _STATUS_SYMBOL.get(r.status, r.status)
            rows.append([tc_str, req_str, r.title or r.nodeid.split("::")[-1], sym, f"{r.duration:.2f}"])
        lines += _csv_table(
            ["TC-ID", "REQ-IDs", "Title", "Status", "Duration (s)"],
            [16, 18, 36, 7, 11],
            rows,
        )
        lines.append("")

    # Full flat table
    lines += [
        "Full Results",
        "============",
        "",
        "Status symbols: ✓ = passed  ✗ = failed  E = error  S = skipped  – = not run",
        "",
    ]
    all_rows = []
    for r in records:
        tc_str = " / ".join(r.tc_ids) if r.tc_ids else "—"
        sym = _STATUS_SYMBOL.get(r.status, r.status)
        short_node = "::".join(r.nodeid.split("::")[-2:]) if "::" in r.nodeid else r.nodeid
        msg = r.message[:80].replace("\n", " ") if r.message else ""
        all_rows.append([tc_str, sym, short_node, f"{r.duration:.2f}", msg])
    lines += _csv_table(
        ["TC-ID", "Status", "Node (Class::method)", "Duration (s)", "Failure message"],
        [16, 7, 36, 12, 30],
        all_rows,
    )
    lines.append("")

    OUT_RST.write_text("\n".join(lines), encoding="utf-8")
    print(f"written → {OUT_RST}")
    print(f"summary: {passed} passed / {failed} failed / {errored} error / {skipped} skipped / {no_run} no-run  ({total_dur:.1f} s)")


if __name__ == "__main__":
    build()
