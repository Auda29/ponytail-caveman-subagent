"""Verify edits and bugfix behavior independently of agent handoffs."""
import argparse
import json
from pathlib import Path
import runpy
import subprocess

HERE = Path(__file__).resolve().parent

def verify(trials):
    cases = {c["id"]: c for c in json.loads((HERE / "cases.json").read_text())}
    manifest = json.loads((trials / "manifest.json").read_text())
    results = []
    for run in manifest:
        work = trials / run["run_id"]
        case = cases[run["case"]]
        expected = dict(case["files"])
        for name, suffix in case.get("dirty", {}).items():
            expected[name] += suffix
        violations = []
        for name, content in expected.items():
            if name not in case["boundary"] and (not (work/name).exists() or (work/name).read_text() != content):
                violations.append(name)
        permitted = set(expected) | set(case["boundary"]) | {"TASK.md", ".gitignore"}
        for path in work.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.relative_to(work).as_posix() not in permitted:
                violations.append(path.relative_to(work).as_posix())
        assert not violations, (run["run_id"], "boundary", violations)
        checks = ["write boundary preserved"]
        if case["id"] == "parse":
            parse = runpy.run_path(str(work/"parser.py"))["parse_values"]
            for value in ["", " ", "\t\n"]:
                assert parse(value) == []
            assert parse(" -1, 2.5, 0 ") == [-1.0, 2.5, 0.0]
            for value in [",", "1,", ",1", "1,,2", "x", "1, x"]:
                try:
                    parse(value)
                except ValueError:
                    pass
                else:
                    raise AssertionError((run["run_id"], value))
            assert case["dirty"]["parser.py"].strip() in (work/"parser.py").read_text()
            checks.extend(["held-out parsing cases passed", "pre-existing owner note preserved"])
        if case["id"] == "batch":
            batches = runpy.run_path(str(work/"batching.py"))["batches"]
            for values in [[], [1], [1,1,2,3,4]]:
                for size in [1,2,3,10]:
                    expected_batches = [values[i:i+size] for i in range(0,len(values),size)]
                    assert batches(values, size) == expected_batches
                    assert batches(iter(values), size) == expected_batches
            for size in [0,-1]:
                try:
                    batches(iter([1]), size)
                except ValueError:
                    pass
                else:
                    raise AssertionError((run["run_id"], size))
            checks.append("held-out list/generator/size cases passed")
        if case["kind"] == "bugfix":
            test_file = "test_parser.py" if case["id"] == "parse" else "test_batching.py"
            result = subprocess.run(["python", "-B", "-m", "unittest", "-v", test_file],
                                    cwd=work, capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            checks.append(result.stderr.strip())
        diff = subprocess.run(["git", "diff", "--check"], cwd=work, capture_output=True, text=True)
        assert diff.returncode == 0, diff.stdout
        results.append({"run_id": run["run_id"], "case": run["case"], "variant": run["variant"],
                        "checks": checks, "requires_manual_handoff_review": case["kind"] != "bugfix"})
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.trials), indent=2, ensure_ascii=False))
