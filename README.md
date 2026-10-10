# Ponytail Caveman Subagent

A delegation skill for bounded coding, debugging, review, and research tasks. It separates the parent agent's coordination rules from the worker's instructions: implement the smallest complete solution, preserve required checks and safeguards, and return a compact, evidence-based handoff.

## Contents

- [`ponytail-caveman-subagent/SKILL.md`](ponytail-caveman-subagent/SKILL.md): parent-agent instructions and handoff schema.
- [`ponytail-caveman-subagent/references/worker-instructions.md`](ponytail-caveman-subagent/references/worker-instructions.md): worker instructions to pass verbatim with each assignment.
- [`opencode-worker.json`](opencode-worker.json): optional OpenCode worker-agent configuration.
- [`INSTALL.md`](INSTALL.md): installation instructions for OpenCode and Hermes.

## Usage

Follow [INSTALL.md](INSTALL.md) to make the skill available to your agent host. Before delegating, the parent reads the worker instructions and includes their full text with a self-contained assignment specifying the outcome, mode, write boundary, acceptance criteria, required checks, budget, and authorized actions.

The worker returns `done`, `partial`, or `blocked`, with the result, changes or evidence, checks, and open issues. The parent verifies the handoff before reporting completion.

## Limits

This package provides instructions, not an executable agent or a filesystem sandbox. Prompt-defined write boundaries must be enforced by the host when technical isolation is required. The optional OpenCode configuration restricts selected actions; it is not a comprehensive shell sandbox.

The four original package files are preserved unchanged. Installation and host compatibility have not been runtime-tested in this repository.
