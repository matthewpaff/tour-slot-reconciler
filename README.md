# Tour Slot Reconciler

Normalize supplied tour slots and retain the newest nonexpired version.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external service, or network access is required.

## Run

```console
python -m slots_tool --help
python -m slots_tool examples/sample.json
python -m slots_tool --conflicts examples/sample.json
python -m slots_tool --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

`--conflicts` compares the latest nonexpired version of each slot and reports overlapping intervals. It keeps at most 100 overlap details in the output while returning the exact total and a truncation flag.

Requires supplied now seconds and slots [{id,start,end,expires_at,version}] (up to 1000). Times are integer seconds and intervals positive. The highest version per ID wins; equal-version conflicts fail. Expired latest records hide earlier versions rather than resurrecting stale availability. Results sort by start/ID. No provider API, time-zone conversion, hold, or booking occurs.

## Learning focus

Independent concept exercise for modeled blueprint section Z01. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `slots_tool/core.py`: validated parsing, storage, or state transitions.
- `slots_tool/cli.py`: JSON command interface.
- `slots_tool/generate_fixtures.py`: original deterministic validation cases.
- `slots_tool/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 547 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
