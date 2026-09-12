# QA artefacts — playwright v3

Machine-readable exports alongside the Sphinx-rendered QA docs in `../source/qa/`.

| File | Contents |
|---|---|
| [rtm.csv](rtm.csv) | Full RTM: 71 rows (61 REQ × area / feature / test cases / status / priority / notes) |

Open `rtm.csv` in Excel or any CSV viewer.
Filter column `status` for: `automated` · `xfail` · `gap`.
Filter column `priority` for: `H` · `M` · `L`.

The same data is rendered as human-readable tables in the Sphinx docs:
- `docs/source/qa/feature_catalogue.rst` — requirements catalogue
- `docs/source/qa/traceability_matrix.rst` — coverage snapshot
- `docs/source/qa/test_plan.rst` — test plan
