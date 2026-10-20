# Installation

Copy the `ponytail-caveman-subagent/` folder to
`~/.agents/skills/ponytail-caveman-subagent/`. Keep this as the canonical copy.

## OpenCode

OpenCode discovers `~/.agents/skills/`. Merge `agent.worker` from
`opencode-worker.json` into `~/.config/opencode/opencode.json` without replacing
other configuration. The worker now loads its instructions through `prompt`;
the parent supplies only the task when that loading is verified.

The example's `{file:../../.agents/skills/...}` path is relative to the config
file, and assumes the exact locations above. For a custom config directory,
project config, or relocated skill, replace it with the correct relative or
absolute path. Restart the host after updating the worker rules.

Check the resolved file before relying on prompt loading. Then start a fresh
worker with a read-only task and verify it uses the loaded handoff format.
A JSON parse or file-existence check alone does not prove runtime injection.

The configuration restricts selected Git commands and nested delegation; it is
not a shell/filesystem sandbox. Use host isolation for enforced boundaries.
It uses the documented `agent`, `mode`, `prompt`, and `permission` fields;
verify your installed host version before translating to a different format.

Sources: [agents and prompt files](https://opencode.ai/docs/agents/#prompt),
[skill discovery](https://opencode.ai/docs/skills/).

## Hermes and other hosts

For Hermes, add the canonical skill directory to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

Source: [Hermes external skill directories](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/#external-skill-directories).

If the host does not demonstrably load a dedicated worker prompt, the parent
passes `references/worker-instructions.md` in full at the start of each fresh
worker context. Follow-ups reuse it only while that context is preserved.
Reload after reset, uncertain compaction, or an instructions update.

OpenCode and Hermes runtime installation have not been exercised by this
repository's local validation; check on the target host before relying on it.
