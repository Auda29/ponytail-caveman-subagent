"""Prepare isolated task copies; execute each TASK.md with a fresh agent."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def prepare(destination):
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE / "cases.json").read_text())
    rules = {
        "none": "",
        "original": (HERE / "original-worker.md").read_text(),
        "revised": (ROOT / "ponytail-caveman-subagent/references/worker-instructions.md").read_text(),
    }
    manifest = []
    for case in cases:
        for variant, contract in rules.items():
            run_id = f"r{len(manifest)+1:02d}"
            work = destination / run_id
            work.mkdir()
            for name, content in case["files"].items():
                target = work / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            (work / ".gitignore").write_text("__pycache__/\n")
            subprocess.run(["git", "init", "-q", str(work)], check=True)
            subprocess.run(["git", "-C", str(work), "add", "."], check=True)
            subprocess.run(["git", "-C", str(work), "-c", "user.name=Fixture",
                            "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)
            for name, suffix in case.get("dirty", {}).items():
                with (work / name).open("a") as file:
                    file.write(suffix)
            boundary = ", ".join(case["boundary"]) or "none"
            assignment = (
                f"Outcome: {case['outcome']}\nWrite boundary: {boundary}.\n"
                f"Done when: {case['done']}\n"
                "Use only this task directory and its instructions. Local reads/checks "
                "and listed edits are authorized. No network, installs, commits, extra "
                "agents, or edits outside the boundary. Reply in German.\n"
            )
            (work / "TASK.md").write_text((contract + "\n\n" if contract else "") + assignment)
            manifest.append({"run_id": run_id, "case": case["id"], "kind": case["kind"],
                             "variant": variant, "directory": str(work)})
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New directory outside the source checkout")
    args = parser.parse_args()
    prepare(args.destination)
