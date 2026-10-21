---
name: ponytail-caveman-subagent
description: >-
  Delegate bounded coding, debugging, review, or research with minimal complete
  changes and concise, evidence-based handoffs. Use when delegation is already
  allowed and useful; this skill does not authorize or require spawning agents.
---

# Delegate a bounded task

These instructions are for the parent. Worker rules live in
`references/worker-instructions.md`; apply them only to the assigned worker.
Follow host and project instructions. If delegation is unavailable, do the work locally.

## Load the worker rules once

Read the worker instructions and pass their complete text into each fresh worker
context, unless the host demonstrably loads that exact content as its agent prompt.
A name, description, or version label alone is not proof. Reuse the loaded rules
for follow-ups in the same preserved context. After reset, uncertain compaction,
or a rules update, supply the current rules again.

## Give three essentials

- **Outcome:** the problem to solve, with enough context to work independently.
- **Write boundary:** permitted files/directories, or `none`.
- **Done when:** observable acceptance criteria.

Default to read-only review/research; an explicit implementation request permits
edits only inside its boundary. No nested agents, commits, installs, deployment,
or external writes/messages unless authorized. Read-only network research is
allowed when needed by the assignment and permitted by the host.

Add required checks, budgets, decisions, known failures, or special permissions
only when relevant. Resolve missing user decisions before delegation. Give
parallel workers disjoint write boundaries; isolate worktrees or shared build
state when file separation is insufficient.

For a simple read acknowledgement, request at most three lines and no full file
list. Allow extra space for blockers; do not impose that limit on substantive work.

```text
Outcome: Fix the parser crash on an empty list.
Write boundary: src/parser.py and tests/test_parser.py.
Done when: Empty input works; existing parsing behavior is preserved.
```

## Check the result

Check acceptance criteria, evidence, and the worker's attributable diff against
its starting state. Do not attribute concurrent workers' edits to this worker.
Before accepting, check required fields, the task's response limit, and cheap
factual consistency (for example, counts against tool output). Request a targeted
correction for missing fields or contradictions instead of passing them through.
Repeat a decisive check when risk, doubt, or cheap independent confirmation
justifies it; do not repeat every check automatically.

Resolve `partial` or `blocked` work before claiming completion. Preserve missing
checks and uncertainty in the user-facing report. Never upgrade build, simulation,
or proposed-fix evidence into runtime, hardware, or implemented-fix claims.

If the host needs JSON, use `references/handoff.schema.json`; otherwise accept
the worker's compact text format. A schema supplied as text does not enforce
output, and valid structure does not prove factual accuracy. Report the checked
result in your own words.
