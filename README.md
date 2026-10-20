# Ponytail Caveman Subagent

A portable delegation skill: complete a bounded task with a small readable
change and a concise, evidence-based handoff.

- [`SKILL.md`](ponytail-caveman-subagent/SKILL.md): parent coordination.
- [`worker-instructions.md`](ponytail-caveman-subagent/references/worker-instructions.md): worker contract.
- [`handoff.schema.json`](ponytail-caveman-subagent/references/handoff.schema.json): optional machine-readable response schema.
- [`INSTALL.md`](INSTALL.md): host setup and the OpenCode worker prompt.

## Use

Supply an outcome, write boundary, and observable completion criteria. Add
constraints and required checks when relevant. Load worker rules once per fresh
context, either through a verified agent prompt or explicit injection. Follow-up
assignments reuse retained rules. The parent checks the worker's evidence.

The v2 handoff requires `status`, `result`, and `evidence_checks`; `open` is
included when needed. Consumers of the old five-field schema must update their
parser or explicitly supply their existing schema with the assignment.

## Upstream review

Reviewed on 2026-10-20 against
[Ponytail v5.3.2](https://github.com/DietrichGebert/ponytail/tree/v5.3.2)
and [Caveman v4.0.1](https://github.com/JuliusBrussee/caveman/tree/v4.0.1).
This is an independently maintained combination, not an automatic upstream sync.

Relevant principles retained: finish required callers and checks, preserve
protections, document meaningful shortcut limits, support review findings with
concrete cases, and prioritize clear language and exact technical details.
Session modes, dashboards, proxies, and cloud integrations are outside this skill.
No upstream software or runtime dependency is installed by loading it.

## Limits and evaluation

Instructions do not enforce filesystem isolation. Parallel work may also need
separate worktrees or build directories. The OpenCode example restricts selected
actions; it is not a comprehensive shell sandbox.

See [`evaluation/README.md`](evaluation/README.md) for the comparison protocol,
observations, and unmeasured quantities. Shorter instructions alone do not prove
lower whole-session token use, cost, or latency. Target-host OpenCode/Hermes
runtime compatibility remains unverified here.
