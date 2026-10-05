from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETS = ("Y_test_data", "N_test_data")
STANDARD_CASE = "092"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def merge_ordered(required: dict, existing: dict) -> dict:
    merged = dict(required)
    for key, value in existing.items():
        if key not in merged:
            merged[key] = value
    return merged


def patch_files(patch_text: str) -> list[str]:
    return re.findall(r"^diff --git a/\S+ b/(\S+)$", patch_text, re.MULTILINE)


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def first(*values):
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def normalized_issue_url(repo: str, issue_id, pull_request_id, *candidates) -> str | None:
    explicit = first(*candidates)
    if explicit:
        return explicit
    if pull_request_id is not None:
        return f"https://github.com/{repo}/pull/{pull_request_id}"
    if issue_id is not None:
        return f"https://github.com/{repo}/issues/{issue_id}"
    return None


def standard_layout(case_name: str) -> dict:
    return {
        "schema_version": "2.0",
        "case_directory": case_name,
        "analysis": "analysis/",
        "patches": "patches/",
        "official_swebench": "official_swebench/",
        "evaluator": "evaluator/",
        "verification": "verification/",
    }


def default_provenance(dataset_set: str, repo: str) -> dict:
    upstream = dataset_set == "Y_test_data"
    return {
        "gold_patch_authorship": f"{repo}_upstream",
        "gold_patch_source": "official_upstream_fix_commit",
        "test_patch_source": (
            "official_upstream_regression_test"
            if upstream
            else "dataset_construction_regression_test"
        ),
        "test_patch_authorship": (
            f"{repo}_upstream" if upstream else "dataset_construction"
        ),
        "upstream_regression_test_found": upstream,
        "model_patch_example_source": "copy_of_gold_patch_for_evaluator_smoke_test",
        "model_patch_example_is_model_generated": False,
    }


def ensure_source_row(
    case_dir: Path,
    number: str,
    instance: dict,
    metadata: dict,
    config: dict,
    test_files: list[str],
) -> None:
    path = case_dir / "analysis" / f"source_row_{number}.json"
    existing = read_json(path)
    issue_id = first(instance.get("issue_id"), metadata.get("issue_id"), existing.get("issue_id"))
    pull_request_id = first(instance.get("pull_request_id"), existing.get("pull_request_id"))
    repo = first(instance.get("repo"), metadata.get("repo"))
    issue_url = normalized_issue_url(
        repo,
        issue_id,
        pull_request_id,
        instance.get("issue_url"),
        metadata.get("issue_url"),
        existing.get("issue_url"),
    )
    fix_commit = first(instance.get("fix_commit"), metadata.get("fix_commit"), config.get("fix_commit"))
    required = {
        "instance_id": instance.get("instance_id"),
        "source_project": repo,
        "source_case": number,
        "language_pair": "Java-C",
        "repo": repo,
        "issue_id": issue_id,
        "issue_url": issue_url,
        "commit": fix_commit,
        "base_commit": instance.get("base_commit"),
        "base_commit_status": "verified" if metadata.get("verification", {}).get("base_fails") else "recorded",
        "fix_commit": fix_commit,
        "commit_url": f"https://github.com/{repo}/commit/{fix_commit}",
        "problem_statement": instance.get("problem_statement"),
        "test_source": metadata.get("test_source"),
        "test_files": test_files,
        "verification_status": (
            "resolved"
            if metadata.get("verification", {}).get("base_fails")
            and metadata.get("verification", {}).get("fix_passes")
            else first(existing.get("verification_status"), "pending")
        ),
        "FAIL_TO_PASS": as_list(instance.get("FAIL_TO_PASS")),
        "PASS_TO_PASS_COUNT": len(as_list(instance.get("PASS_TO_PASS"))),
    }
    write_json(path, merge_ordered(required, existing))


def ensure_environment_spec(
    case_dir: Path,
    instance: dict,
    metadata: dict,
    config: dict,
    test_files: list[str],
) -> None:
    path = case_dir / "analysis" / "environment_spec.json"
    existing = read_json(path)
    verification = metadata.get("verification", {})
    runtime_verified = first(existing.get("runtime_verified"), verification.get("docker_verified"), False)
    required = {
        "instance_id": instance.get("instance_id"),
        "task_level": first(existing.get("task_level"), "integration"),
        "validation_type": first(existing.get("validation_type"), "base_fix_regression"),
        "environment": first(existing.get("environment"), existing.get("base_image"), config.get("image")),
        "python_version_target": first(existing.get("python_version_target"), existing.get("python"), config.get("python_version")),
        "java_requirement": first(existing.get("java_requirement"), existing.get("java"), "case-specific JDK"),
        "native_requirement": first(existing.get("native_requirement"), "case-specific native build toolchain"),
        "build_system": first(existing.get("build_system"), "repository build system at Base commit"),
        "test_execution": first(existing.get("test_execution"), existing.get("test_command"), metadata.get("test_command"), instance.get("test_command")),
        "runtime_verified": bool(runtime_verified),
        "notes": as_list(existing.get("notes")),
        "reproduction_status": first(
            existing.get("reproduction_status"),
            "resolved" if verification.get("base_fails") and verification.get("fix_passes") else "pending",
        ),
        "base_commit": instance.get("base_commit"),
        "fix_commit": metadata.get("fix_commit"),
        "test_source": metadata.get("test_source"),
        "test_files": test_files,
        "FAIL_TO_PASS": as_list(instance.get("FAIL_TO_PASS")),
        "PASS_TO_PASS_COUNT": len(as_list(instance.get("PASS_TO_PASS"))),
        "verification": verification,
    }
    write_json(path, merge_ordered(required, existing))


def ensure_case_readme(case_dir: Path, number: str, instance: dict, metadata: dict) -> None:
    path = case_dir / "README.md"
    current = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if "## Directory contract" in current and "## Public/private separation" in current:
        return
    test_source = metadata.get("test_source", "recorded regression test")
    addition = f"""

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: config-driven isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, run, grading, and control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_{number}.json`. The
complete private instance, gold patch, protected test patch, and expected test
outcomes must not be shown during an unbiased model evaluation. Test provenance
is recorded as `{test_source}` in `official_swebench/metadata.json`.
"""
    path.write_text(current.rstrip() + addition, encoding="utf-8", newline="\n")


def ensure_analysis_readme(case_dir: Path, number: str, instance: dict, metadata: dict) -> None:
    path = case_dir / "analysis" / "README.md"
    if path.exists():
        return
    verification = metadata.get("verification", {})
    text = f"""# Case {number} analysis

## Identity

- Instance: `{instance.get('instance_id')}`
- Repository: `{instance.get('repo')}`
- Base: `{instance.get('base_commit')}`
- Fix: `{metadata.get('fix_commit')}`
- Test source: `{metadata.get('test_source')}`

## Construction and verification

The production patch is stored in `patches/gold_patch.diff`; the protected
regression test is stored in `patches/test_patch.diff`. The evaluator applies a
candidate model patch first and the protected test patch second to a clean Base
checkout. Recorded verification status: Base fails =
`{verification.get('base_fails')}`, Fix passes = `{verification.get('fix_passes')}`.
`FAIL_TO_PASS` and `PASS_TO_PASS` are stored in the private instance and metadata.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def ensure_evaluator_docs(case_dir: Path, number: str) -> None:
    evaluator = case_dir / "evaluator"
    readme = evaluator / "README.md"
    if not readme.exists():
        readme.write_text(
            f"""# Case {number} isolated model-patch evaluator

The evaluator follows the case-092 isolation contract. Case-specific behavior
is limited to `case_config.json`, `case_adapter.sh`, and `image/Dockerfile`.
The image contains a clean checkout at Base and no gold patch, protected test
patch, Fix source, expected outcomes, or evaluation entrypoint.

Runtime order:

```text
clean Base -> model patch -> protected test patch -> build -> tests -> grade
```

Build evidence is written to `verification/builds/<build-id>/`; evaluation
evidence is written to `verification/runs/<run-id>/`.
""",
            encoding="utf-8",
            newline="\n",
        )
    logging = evaluator / "LOGGING.md"
    if not logging.exists():
        reference = ROOT / "Y_test_data" / "javac_case_092" / "evaluator" / "LOGGING.md"
        logging.write_text(reference.read_text(encoding="utf-8-sig"), encoding="utf-8", newline="\n")
    dockerignore = evaluator / "image" / ".dockerignore"
    if not dockerignore.exists():
        dockerignore.write_text("*\n!Dockerfile\n", encoding="utf-8", newline="\n")


def ensure_verification_docs(case_dir: Path, number: str) -> None:
    verification = case_dir / "verification"
    verification.mkdir(parents=True, exist_ok=True)
    for child in ("builds", "runs", "controls"):
        (verification / child).mkdir(exist_ok=True)
    readme = verification / "README.md"
    if not readme.exists():
        readme.write_text(
            f"""# Case {number} verification evidence

- `builds/`: immutable image-build and clean-image audit records.
- `runs/`: isolated candidate, Base-control, and gold-control evaluations.
- `controls/`: non-fixing control patches used to prove Base failure.

Each run records raw logs, structured events, a phase result, per-test grading,
and a summary. A valid official-test case must show that the Base control fails
the recorded `FAIL_TO_PASS`, while the upstream gold patch passes all expected
`FAIL_TO_PASS` and `PASS_TO_PASS` targets.
""",
            encoding="utf-8",
            newline="\n",
        )


def official_readme(number: str, instance: dict, metadata: dict) -> str:
    provenance = metadata.get("patch_provenance", {})
    return f"""# SWE-bench-compatible record: case {number}

- Canonical JSON: `instance_{number}.json`
- JSONL: `instance_{number}.jsonl`
- Instance ID: `{instance.get('instance_id')}`
- Repository: `{instance.get('repo')}`
- Base commit: `{instance.get('base_commit')}`
- Fix commit: `{metadata.get('fix_commit')}`
- Project version: `{instance.get('version')}`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `{provenance.get('gold_patch_source')}`.
- `test_patch.diff`: `{provenance.get('test_patch_source')}`.
- Test authorship: `{provenance.get('test_patch_authorship')}`.

## Public/private separation

`public_task_{number}.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
"""


def write_checksums(official: Path, number: str) -> None:
    names = [
        f"instance_{number}.json",
        f"instance_{number}.jsonl",
        "metadata.json",
        f"public_task_{number}.json",
        "README.md",
    ]
    lines = []
    for name in names:
        data = (official / name).read_bytes()
        lines.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
    (official / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def normalize_case(dataset_set: str, case_dir: Path) -> None:
    number = case_dir.name.removeprefix("javac_case_")
    if number == STANDARD_CASE:
        write_checksums(case_dir / "official_swebench", number)
        return

    official = case_dir / "official_swebench"
    instance_path = official / f"instance_{number}.json"
    instance = read_json(instance_path)
    if not instance:
        raise RuntimeError(f"Missing canonical instance: {instance_path}")
    config = read_json(case_dir / "evaluator" / "case_config.json")
    metadata_path = official / "metadata.json"
    metadata = read_json(metadata_path)
    source_path = case_dir / "analysis" / f"source_row_{number}.json"
    source_row = read_json(source_path)
    environment = read_json(case_dir / "analysis" / "environment_spec.json")

    gold_patch = (case_dir / "patches" / "gold_patch.diff").read_text(encoding="utf-8-sig")
    test_patch = (case_dir / "patches" / "test_patch.diff").read_text(encoding="utf-8-sig")
    repo = first(instance.get("repo"), metadata.get("repo"), source_row.get("repo"))
    fix_commit = first(instance.get("fix_commit"), metadata.get("fix_commit"), source_row.get("fix_commit"), config.get("fix_commit"))
    issue_id = first(instance.get("issue_id"), metadata.get("issue_id"), source_row.get("issue_id"))
    pull_request_id = first(instance.get("pull_request_id"), source_row.get("pull_request_id"))
    issue_url = normalized_issue_url(
        repo,
        issue_id,
        pull_request_id,
        instance.get("issue_url"),
        metadata.get("issue_url"),
        source_row.get("issue_url"),
    )
    test_files = as_list(first(instance.get("test_files"), metadata.get("test_files"), environment.get("test_files"), patch_files(test_patch)))
    pass_to_pass = as_list(instance.get("PASS_TO_PASS"))
    fail_to_pass = as_list(instance.get("FAIL_TO_PASS"))
    test_command = first(instance.get("test_command"), metadata.get("test_command"), metadata.get("test_command_effective"), environment.get("test_execution"), environment.get("test_command"))

    verification = dict(metadata.get("verification", {}))
    if "base_fails" not in verification and environment.get("runtime_verified"):
        verification["base_fails"] = True
    if "fix_passes" not in verification and environment.get("runtime_verified"):
        verification["fix_passes"] = True
    verification.setdefault("template_version", "1.0")
    verification.setdefault("evaluation_assets_injected_at_runtime", True)
    verification.setdefault("image_contains_test_patch", False)
    verification.setdefault("image_contains_gold_patch", False)
    verification.setdefault("image_contains_fix_commit", False)

    provenance = dict(default_provenance(dataset_set, repo))
    provenance.update(metadata.get("patch_provenance", {}))
    test_source_default = (
        "official_upstream_regression_test"
        if dataset_set == "Y_test_data"
        else "dataset_construction_regression_test"
    )
    metadata_required = {
        "dataset_schema_version": "1.0",
        "source_case": number,
        "dataset_variant": "SWE-bench-compatible custom record",
        "test_source": first(metadata.get("test_source"), test_source_default),
        "created_at_source": first(metadata.get("created_at_source"), "recorded upstream issue or change date"),
        "PASS_TO_PASS_COUNT": len(pass_to_pass),
        "created_at": instance.get("created_at"),
        "FAIL_TO_PASS": fail_to_pass,
        "version": instance.get("version"),
        "issue_url": issue_url,
        "PASS_TO_PASS": pass_to_pass,
        "standard_layout": standard_layout(case_dir.name),
        "verification": verification,
        "test_command": test_command,
        "base_commit": instance.get("base_commit"),
        "repo": repo,
        "patch_provenance": provenance,
        "fix_commit": fix_commit,
        "instance_id": instance.get("instance_id"),
        "issue_id": issue_id,
        "test_files": test_files,
        "project_version": instance.get("version"),
        "model_evaluator_image": config.get("image"),
    }
    metadata = merge_ordered(metadata_required, metadata)

    instance_required = {
        "version": instance.get("version"),
        "test_patch": test_patch,
        "hints_text": first(instance.get("hints_text"), ""),
        "problem_statement": instance.get("problem_statement"),
        "FAIL_TO_PASS": fail_to_pass,
        "patch": gold_patch,
        "base_commit": instance.get("base_commit"),
        "instance_id": instance.get("instance_id"),
        "repo": repo,
        "created_at": instance.get("created_at"),
        "issue_id": issue_id,
        "issue_url": issue_url,
        "PASS_TO_PASS": pass_to_pass,
        "fix_commit": fix_commit,
        "test_files": test_files,
        "test_command": test_command,
    }
    if pull_request_id is not None:
        instance_required["pull_request_id"] = pull_request_id
    instance = merge_ordered(instance_required, instance)

    write_json(instance_path, instance)
    (official / f"instance_{number}.jsonl").write_text(
        json.dumps(instance, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(metadata_path, metadata)

    public_task = {
        "instance_id": instance.get("instance_id"),
        "repo": repo,
        "base_commit": instance.get("base_commit"),
        "problem_statement": instance.get("problem_statement"),
        "hints_text": first(instance.get("hints_text"), ""),
        "created_at": instance.get("created_at"),
        "version": instance.get("version"),
        "issue_id": issue_id,
        "issue_url": issue_url,
        "project_version": instance.get("version"),
    }
    if pull_request_id is not None:
        public_task["pull_request_id"] = pull_request_id
    write_json(official / f"public_task_{number}.json", public_task)

    ensure_source_row(case_dir, number, instance, metadata, config, test_files)
    ensure_environment_spec(case_dir, instance, metadata, config, test_files)
    ensure_case_readme(case_dir, number, instance, metadata)
    ensure_analysis_readme(case_dir, number, instance, metadata)
    ensure_evaluator_docs(case_dir, number)
    ensure_verification_docs(case_dir, number)
    (official / "README.md").write_text(
        official_readme(number, instance, metadata), encoding="utf-8", newline="\n"
    )
    write_checksums(official, number)


def main() -> None:
    normalized = []
    for dataset_set in SETS:
        for case_dir in sorted((ROOT / dataset_set).glob("javac_case_*")):
            normalize_case(dataset_set, case_dir)
            if case_dir.name != f"javac_case_{STANDARD_CASE}":
                normalized.append(f"{dataset_set}/{case_dir.name}")
    print(json.dumps({"normalized": normalized, "template": "javac_case_092"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
