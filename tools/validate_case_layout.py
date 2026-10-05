from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETS = ("Y_test_data", "N_test_data")

INSTANCE_KEYS = {
    "instance_id",
    "repo",
    "base_commit",
    "patch",
    "test_patch",
    "problem_statement",
    "hints_text",
    "created_at",
    "version",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
}
METADATA_KEYS = {
    "dataset_schema_version",
    "source_case",
    "dataset_variant",
    "test_source",
    "PASS_TO_PASS_COUNT",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
    "standard_layout",
    "verification",
    "base_commit",
    "fix_commit",
    "repo",
    "patch_provenance",
    "instance_id",
    "test_files",
    "project_version",
}
SOURCE_KEYS = {
    "instance_id",
    "source_case",
    "language_pair",
    "repo",
    "base_commit",
    "fix_commit",
    "commit_url",
    "problem_statement",
    "test_source",
    "test_files",
    "FAIL_TO_PASS",
}
ENVIRONMENT_KEYS = {
    "instance_id",
    "task_level",
    "validation_type",
    "environment",
    "python_version_target",
    "java_requirement",
    "build_system",
    "test_execution",
    "runtime_verified",
    "reproduction_status",
    "base_commit",
    "fix_commit",
    "test_source",
    "test_files",
    "FAIL_TO_PASS",
    "PASS_TO_PASS_COUNT",
    "verification",
}
FORBIDDEN_PUBLIC_KEYS = {
    "patch",
    "test_patch",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
    "fix_commit",
    "test_files",
    "test_command",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    number = case_dir.name.removeprefix("javac_case_")
    official = case_dir / "official_swebench"
    required_files = [
        case_dir / "README.md",
        case_dir / "analysis" / "README.md",
        case_dir / "analysis" / "environment_spec.json",
        case_dir / "analysis" / f"source_row_{number}.json",
        case_dir / "patches" / "gold_patch.diff",
        case_dir / "patches" / "test_patch.diff",
        official / f"instance_{number}.json",
        official / f"instance_{number}.jsonl",
        official / f"public_task_{number}.json",
        official / "metadata.json",
        official / "README.md",
        official / "SHA256SUMS.txt",
        case_dir / "evaluator" / "case_config.json",
        case_dir / "evaluator" / "case_adapter.sh",
        case_dir / "evaluator" / "image" / "Dockerfile",
        case_dir / "evaluator" / "image" / ".dockerignore",
        case_dir / "evaluator" / "README.md",
        case_dir / "evaluator" / "LOGGING.md",
        case_dir / "evaluator" / "build_model_evaluator.py",
        case_dir / "evaluator" / "evaluate_model_patch.py",
        case_dir / "evaluator" / "run_evaluation.sh",
        case_dir / "verification" / "README.md",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"missing {path.relative_to(case_dir)}")
    if errors:
        return errors

    instance = load(official / f"instance_{number}.json")
    jsonl = load(official / f"instance_{number}.jsonl")
    metadata = load(official / "metadata.json")
    public = load(official / f"public_task_{number}.json")
    source = load(case_dir / "analysis" / f"source_row_{number}.json")
    environment = load(case_dir / "analysis" / "environment_spec.json")

    if instance != jsonl:
        errors.append("instance JSON and JSONL differ")
    if missing := INSTANCE_KEYS - instance.keys():
        errors.append(f"instance missing keys: {sorted(missing)}")
    if missing := METADATA_KEYS - metadata.keys():
        errors.append(f"metadata missing keys: {sorted(missing)}")
    if missing := SOURCE_KEYS - source.keys():
        errors.append(f"source row missing keys: {sorted(missing)}")
    if "verification_status" not in source and "verification" not in source:
        errors.append("source row lacks verification status/details")
    if "PASS_TO_PASS_COUNT" not in source and "PASS_TO_PASS" not in source:
        errors.append("source row lacks PASS_TO_PASS count/list")
    if missing := ENVIRONMENT_KEYS - environment.keys():
        errors.append(f"environment spec missing keys: {sorted(missing)}")
    if leaked := FORBIDDEN_PUBLIC_KEYS & public.keys():
        errors.append(f"public task leaks private keys: {sorted(leaked)}")

    gold_patch = (case_dir / "patches" / "gold_patch.diff").read_text(encoding="utf-8-sig")
    test_patch = (case_dir / "patches" / "test_patch.diff").read_text(encoding="utf-8-sig")
    if instance.get("patch") != gold_patch:
        errors.append("embedded gold patch differs from patches/gold_patch.diff")
    if instance.get("test_patch") != test_patch:
        errors.append("embedded test patch differs from patches/test_patch.diff")
    if metadata.get("PASS_TO_PASS_COUNT") != len(instance.get("PASS_TO_PASS", [])):
        errors.append("PASS_TO_PASS_COUNT does not match instance")
    if metadata.get("FAIL_TO_PASS") != instance.get("FAIL_TO_PASS"):
        errors.append("metadata FAIL_TO_PASS does not match instance")
    if metadata.get("PASS_TO_PASS") != instance.get("PASS_TO_PASS"):
        errors.append("metadata PASS_TO_PASS does not match instance")

    checksum_path = official / "SHA256SUMS.txt"
    for raw_line in checksum_path.read_text(encoding="utf-8-sig").splitlines():
        expected, name = raw_line.split("  ", 1)
        target = official / name
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"checksum mismatch: {name}")
    return errors


def main() -> None:
    results = {}
    for dataset_set in SETS:
        for case_dir in sorted((ROOT / dataset_set).glob("javac_case_*")):
            key = f"{dataset_set}/{case_dir.name}"
            results[key] = validate_case(case_dir)
    failed = {key: value for key, value in results.items() if value}
    print(json.dumps({"cases": len(results), "failed": failed}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
