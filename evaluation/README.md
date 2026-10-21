# Worker comparison — 2026-10-20

For the follow-up on counts, required fields, response length, and parent
acceptance, see [Handoff regression checks](#handoff-regression-checks--2026-10-21).
The comparison and size measurements below describe the original v2 revision.

The shortened contract preserved the expected behavior in this small comparison.
All three variants met the six task rubrics. This does not demonstrate an
improvement in quality, whole-session cost, or latency.

## Method

- Six small fixtures: two bug fixes, two read-only reviews, two document-based
  research tasks. Each ran once with no added worker contract, the original
  contract, and the revised contract: 18 fresh subagents, no conversation fork.
- Agents inherited the same parent model/effort settings and tool environment;
  no per-run overrides. A pinned provider model identifier and usage counters
  were not exposed by the agent interface, limiting external reproducibility.
- Each received the same launch instruction with its own opaque task directory:
  `Read <directory>/TASK.md and carry out that assignment. Work only in
  <directory> and follow the task's instructions. Return your handoff in the
  final answer.` TASK.md contained the variant's full worker text, then the same
  task-specific assignment. The baseline omitted only the worker text.
- Separate fixture repositories prevented accidental source sharing. Workers
  were instructed to stay within their task directory; this was not a technical
  sandbox. They received no expected answers, diagnosis, sibling outputs, or
  evaluator script. Runs overlapped; timings were not treated as comparable.
- The parent independently ran held-out bugfix assertions and the resulting
  unit tests, checked diffs and preservation of an existing owner comment, and
  manually reviewed findings and research claims against the source fixtures.
  No worker required a corrective follow-up.

The original worker is preserved in `original-worker.md`, from repository
commit `3c377402c0c909c2764c8664c07e1a522775d677`, blob
`1cc0e480daee4b1bde657013efc36c48d7a2a290`.

## Observations

| Task / rubric | No added contract | Original | Revised |
|---|---|---|---|
| Empty parser input; retain invalid-field errors and owner comment | Pass | Pass | Pass |
| Single-use generators; preserve order, batches, size validation | Pass | Pass | Pass |
| Identify tenant-prefix access and expiry-boundary defects | Pass | Pass | Pass |
| Identify export-root sibling-prefix escape without editing | Pass | Pass | Pass |
| Resolve 750 ms override vs 500/1000 ms defaults; no hardware proof | Pass | Pass | Pass |
| Do not invent gateway model/firmware; identify exact missing facts | Pass | Pass | Pass |

All six implementations passed independent behavior checks. All twelve
review/research runs preserved fixture source files. Review handoffs contained
concrete failure cases; research handoffs preserved uncertainty and units.

The original firmware-research run returned `partial`; the revised run returned
`done` with an explicit `Open` field for missing model/firmware. Both met this
task's acceptance criterion of reporting an evidence gap. Neither established
that the actual gateway supports 50 ms. Status alone must not be treated as
proof of compatibility.

## Size measurements

Character counts are Unicode code points including whitespace; words use
Python `str.split()`. These are not tokenizer or billing measurements.

| Instruction file | Original characters | Revised characters | Reduction |
|---|---:|---:|---:|
| Parent SKILL.md, including metadata and old inline schema | 4,129 | 2,651 | 35.8% |
| Worker instructions | 6,326 | 3,893 | 38.5% |

The revised JSON schema is loaded separately when needed; its size is excluded
from the revised parent-file figure. Moving it explains part of that reduction.

| Six final handoffs combined | Words | Characters |
|---|---:|---:|
| No added contract | 486 | 4,705 |
| Original | 563 | 5,107 |
| Revised | 533 | 5,017 |

The revised handoffs were only slightly shorter than the original in this run;
the baseline was shortest and also passed. Simple tasks therefore do not establish
a need for this skill. The clearest measured saving is the smaller instruction
text, not demonstrated cheaper execution.

## Evidence and reproduction

- `cases.json`: original tasks and files, without expected answers.
- `handoffs.json`: captured final responses. Sandbox links refer to the original
  ephemeral run locations; fixture filenames and cases remain available here.
- `verification.json`: independent file/boundary checks and final unit-test output.
- `changes.json`: final implementation diffs; parser diffs include the pre-existing
  owner note, which `cases.json` distinguishes from worker changes.

From the repository root, create a new directory outside the checkout:

```sh
python evaluation/prepare.py /tmp/ponytail-trials
```

Start one fresh agent per generated TASK.md with the launch instruction above.
Use the same model, effort, tools, permissions, and source state. Do not show
agents this report or `verify.py`. Capture final responses, then run:

```sh
python evaluation/verify.py /tmp/ponytail-trials
```

The verifier asserts bugfix behavior and source boundaries. Review/research
grading still requires reading the handoffs against the table above.

## Limits and remaining measurements

This is a worker-contract smoke comparison, not an end-to-end parent/worker
benchmark. It does not exercise parent prompt construction, context retention,
compaction, missing write authorization, shared build-state collisions, or actual
OpenCode/Hermes prompt injection. JSON, the documented relative prompt path,
and skill frontmatter were checked locally; host binaries were unavailable.

Total input/output/reasoning/cache tokens, parent overhead, billed cost, and
reliable per-run latency were unavailable and are deliberately not estimated.
For a full host comparison, run all three variants through the actual parent,
record these counters plus correctness and rework, rotate variant order, and
repeat tasks with fresh contexts. One run per small fixture cannot establish
statistical reliability or behavior across models and large projects.

## Handoff regression checks — 2026-10-21

The follow-up checks three dimensions separately: required fields, numeric
consistency with a Git inventory, and the task-specific response limit. These
address the reported read-only run with wrong totals, a missing `Status`, and
unnecessarily long acknowledgements; they do not rerun its four-model setup.

`check_read_handoff.py` checks the successful-read benchmark's three-line text
format: `Status`, `Result`, and `Evidence/checks`, with one `files_read=N` token
in the evidence field. Separate the token with whitespace or a semicolon. It
compares N with the frozen fixture's NUL-delimited Git inventory, including
filenames containing newlines. Run the regression suite from the repository root:

```sh
python -B -m unittest discover -s evaluation -p test_read_handoff.py -v
python -B evaluation/check_read_handoff.py /path/to/frozen-repo /path/to/handoff.txt
```

The checker is an offline evaluation tool, not a runtime hook or proof that files
were read. It checks status syntax, not whether `done` is justified. A blocked
task may legitimately need a longer response and requires separate assessment.
Keep the fixture inventory unchanged between assignment and checking; inspect
read coverage and source changes independently.

The ten unit tests cover the reported totals of 13/14 versus 15, missing/empty or
duplicate fields, invalid status, excessive length, conflicting or malformed
counts, a valid acknowledgement, and Git counting with unusual filenames and
an untracked file. Fresh-agent inputs, outputs, independent fixture checks, and
reproduction instructions are recorded in `handoff-checks.json`.

Both fresh-agent checks passed: the worker returned the correct count in three
lines, and the parent rejected the supplied wrong count, missing status, and
overlong file list with a targeted correction request. Both fixture inventories
and content hashes remained unchanged. These are single smoke checks without a
baseline; they establish neither comparative improvement nor actual read coverage.
