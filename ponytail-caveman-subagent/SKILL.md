---
name: ponytail-caveman-subagent
description: >-
  Rules for delegating a bounded coding, debugging, review, or research task to
  a subagent: how to write the assignment, how to pass the worker instructions
  verbatim, and how to evaluate the compact handoff. Use whenever you are about
  to delegate such a task and delegation is already allowed; this skill never
  by itself justifies delegating.
---

# Delegation: Minimal Solution, Compact Handoff

This file is for the delegating (parent) agent. The subagent's rules are in
`references/worker-instructions.md`. Do not apply those rules to your own work;
you coordinate, write assignments, and evaluate results.

## 1. Whether to delegate is decided elsewhere

Delegate only when the user, the host, and its configuration allow it and the
task can be described completely in one bounded assignment. If delegation is
not allowed or not supported, do the work yourself and do not mention this
skill. Do not delegate a task that first needs a decision from the user; get
the decision, then delegate.

## 2. Pass the worker instructions

- Read `references/worker-instructions.md` (through the host's skill tool if
  it loads skill files, otherwise as a file) and put its full text verbatim
  into the subagent's prompt or context, before the assignment.
- Do this on every delegation, even if a subagent type seems to carry the
  instructions already. A description is not proof; a duplicate costs a few
  tokens, a missing block costs the limits you are delegating.
- Never summarize, shorten, or paraphrase it.
- If the host accepts an output schema, also pass the handoff schema below.

## 3. Write the assignment

Do not assume the subagent can see your conversation history. Every
assignment is self-contained and states:

- **Outcome:** what must be true when the task is done.
- **Mode:** implement, review, or research.
- **Write boundary:** the files or directories it may edit; none for review or
  research.
- **Acceptance criteria:** how done is recognized.
- **Required checks:** exact commands, if any.
- **Budget:** limits on time, iterations, or sources, if any.
- **Authorized actions:** anything beyond local edits and checks (commit,
  network, installing packages, external services). Default: none.
- **Context it cannot discover itself:** decisions already made, user
  constraints, known failures, relevant paths.

Parallel subagents get disjoint write boundaries. If two tasks need the same
file, run them one after the other or merge them into one assignment.

## 4. Evaluate the handoff

Treat a handoff as a claim, not as a result. Check in proportion to the stakes.

- **done:** confirm the acceptance criteria against the reported evidence. Look
  at the diff for edits outside the write boundary. Rerun a decisive check
  yourself when the claim matters and the check is cheap.
- **partial / blocked:** resolve before reporting completion. Answer the
  question and delegate again, ask the user for a missing decision or
  permission, or finish the remaining work yourself. Anything still open goes
  to the user explicitly.
- Never upgrade the subagent's evidence: unperformed checks stay unperformed,
  a build stays a build, a proposed fix stays a proposal.
- Report to the user in your own words; quote the handoff only when its exact
  wording matters.

## Handoff schema

For hosts that accept an output schema. It matches the text format in the
worker instructions.

```json
{
  "type": "object",
  "required": ["status", "result", "changes_evidence", "checks", "open"],
  "properties": {
    "status": { "enum": ["done", "partial", "blocked"] },
    "result": { "type": "string", "description": "Outcome; decisive cause or finding when relevant" },
    "changes_evidence": { "type": "string", "description": "Edited paths, or findings with code locations / source links" },
    "checks": { "type": "string", "description": "Commands with baseline vs. final results; what was not run and why" },
    "open": { "type": "string", "description": "Assumptions, unresolved dependencies, risks, blocking questions; 'none' if none" }
  }
}
```
