# Installation

## 1. Skill (all hosts)

Copy the folder to one fixed location:

```
~/.agents/skills/ponytail-caveman-subagent/
├── SKILL.md
└── references/worker-instructions.md
```

- **OpenCode (V1):** discovers `~/.agents/skills/` automatically.
- **Hermes:** add the directory to `~/.hermes/config.yaml`:

  ```yaml
  skills:
    external_dirs:
      - ~/.agents/skills
  ```

Keep only this one copy; do not duplicate it into other skill directories.

## 2. OpenCode worker agent (optional)

Merge the `agent.worker` block from `opencode-worker.json` into
`~/.config/opencode/opencode.json`. It adds a subagent with permission limits
(no nested agents, no `git push`/`git clean`, confirmation for commit, reset,
checkout, restore, stash). It carries no prompt of its own: the parent passes
the worker instructions on every delegation, as `SKILL.md` requires.

The block uses the V1 config format. OpenCode V2 (beta) translates V1 config;
if you convert the file to V2 fields, convert all of it; the V2 docs advise
against mixing V1 and V2 field names in one file.
