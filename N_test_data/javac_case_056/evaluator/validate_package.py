"""Check the case-local layout, serialized records, patches and imported evidence (no Docker)."""
from __future__ import annotations

from datetime import datetime, timezone
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile


CASE = Path(__file__).resolve().parents[1]
DATASET = CASE.parents[1]
CONFIG = json.loads((CASE / "evaluator/case_config.json").read_text(encoding="utf-8"))


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-checksums", action="store_true")
    args = parser.parse_args()
    errors = []
    checks = {}
    checks["default_image_pinned_to_published_digest"] = (
        CONFIG["image"] == "yutu0814/javac-case-056-lwjgl3@" + CONFIG["image_digest"]
        and CONFIG["image_digest"] == "sha256:866ae42ecde1bbcaa0581fabe2380bdea159ed944f565066b7abe1c2922a7669"
    )
    checks["local_build_uses_separate_tag"] = (
        CONFIG["build_image"] == "yutu0814/javac-case-056-lwjgl3:local-rebuild"
    )
    official = CASE / "official_swebench"
    checksummed = [
        "instance_056.json", "instance_056.jsonl", "public_task_056.json", "metadata.json",
        "../patches/gold_patch.diff", "../patches/test_patch.diff",
        "../analysis/test_sources/VkFramebufferCreateInfoTest.java",
    ]
    checksum_text = "".join(
        f"{digest((official / name).read_bytes())}  {name}\n" for name in checksummed
    )
    checksum_path = official / "SHA256SUMS.txt"
    if not checksum_path.exists() or args.refresh_checksums:
        checksum_path.write_text(checksum_text, encoding="utf-8", newline="\n")
    elif checksum_path.read_text(encoding="utf-8") != checksum_text:
        errors.append("Checksum manifest differs from file contents")
    validator_path = DATASET / "tools/validate_case_layout.py"
    spec = importlib.util.spec_from_file_location("case_layout", validator_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    layout_errors = module.validate_case(CASE)
    errors.extend(layout_errors)
    checks["standard_layout"] = not layout_errors
    for path in sorted(CASE.rglob("*.json")):
        if "runs" not in path.parts:
            try:
                load(path)
            except (ValueError, OSError) as error:
                errors.append(f"Invalid JSON {path.relative_to(CASE)}: {error}")
    instance = load(official / "instance_056.json")
    metadata = load(official / "metadata.json")
    checks["test_count"] = len(instance["FAIL_TO_PASS"]) == 2
    checks["p2p_record_consistent"] = instance["PASS_TO_PASS"] == metadata["PASS_TO_PASS"]
    formal = metadata["verification"].get("model_evaluator_verified", False)
    if formal:
        base_result = load(CASE / "verification/runs/case-056-base-1/summary.json")
        fix_result = load(CASE / "verification/runs/case-056-gold-1/summary.json")
        tamper_result = load(CASE / "verification/runs/case-056-tamper-1/summary.json")
        checks["formal_runtime_evidence"] = (
            base_result["status"] == "unresolved"
            and base_result["grading"]["FAIL_TO_PASS"]["failed"] == 2
            and base_result["grading"]["PASS_TO_PASS"]["passed"] == len(instance["PASS_TO_PASS"])
            and fix_result["status"] == "resolved"
            and tamper_result["reason"] == "candidate_conflicts_with_test_patch"
        )
    else:
        checks["verification_not_overstated"] = not metadata["verification"]["formal_case_completed"]
    work = CASE.parent / "java_case_056_new"
    base = CONFIG["base_commit"]
    fix = CONFIG["fix_commit"]

    checks["raw_fix_parent_matches_base"] = (
        f"parent {base}" in (CASE / "analysis/fix_commit.raw.txt").read_text().splitlines()
    )
    provenance = load(CASE / "analysis/commit_provenance.json")
    changed = provenance["changed_files"]
    expected_fix = {item["path"]: item["sha256"] for item in load(CASE / "analysis/fix_materials_manifest.json")}
    checks["complete_gold_patch"] = len(changed) == 16 and (
        digest((CASE / "patches/gold_patch.diff").read_bytes()) == metadata["patch_provenance"]["gold_sha256"])
    try:
        with tempfile.TemporaryDirectory(prefix="case056-patches-") as temporary:
            sparse = Path(temporary)
            for path in changed:
                target = sparse / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((CASE / "analysis/base_materials" / path).read_bytes())
            patch_log = []
            for patch_name in ["test_patch.diff", "gold_patch.diff"]:
                patch = CASE / "patches" / patch_name
                for options in (["--check", "--whitespace=error-all"], []):
                    proc = subprocess.run(
                        ["git", "-c", "core.autocrlf=false", "-C", str(sparse), "apply", *options, str(patch)],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    )
                    patch_log.append(proc.stdout.decode("utf-8", errors="replace"))
                    if proc.returncode:
                        raise ValueError(f"{patch_name} apply failed: {patch_log[-1]}")
            test_bytes = (sparse / CONFIG["test_file"]).read_bytes()
            checks["test_patch_matches_test_source"] = (
                test_bytes == (CASE / "analysis/test_sources/VkFramebufferCreateInfoTest.java").read_bytes()
            )
            checks["gold_applies_to_exact_fix_blobs"] = all(
                digest((sparse / path).read_bytes()) == expected_fix[path] for path in changed
            )
            checks["gold_and_test_patches_apply_together"] = True
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        errors.append(str(error))

    checks["base_log_has_both_failures"] = (
        "RESULT: passed=0, failed=2" in (CASE / "verification/generation_evidence/base-tests.raw.log").read_text()
    )
    checks["fix_log_has_both_passes"] = (
        "RESULT: passed=2, failed=0" in (CASE / "verification/generation_evidence/fix-tests.raw.log").read_text()
    )
    log_mapping = {
        "ant-init.log": "ant-init.raw.log",
        "ant-compile-templates.log": "ant-compile-templates.raw.log",
        "ant-compile-parent.log": "ant-compile-parent.raw.log",
        "test-parent.log": "testng-report-infrastructure.raw.log",
        "test-parent-detail.log": "base-tests.raw.log",
        "test-fixed-detail.log": "fix-tests.raw.log",
        "vulkan-parent-repro.log": "original-validator-repro.raw.log",
    }
    evidence_manifest = []
    for source_name, archived_name in log_mapping.items():
        archived = (CASE / "verification/generation_evidence" / archived_name).read_bytes()
        if (work / source_name).is_file() and (work / source_name).read_bytes() != archived:
            errors.append(f"Imported raw log differs: {archived_name}")
        evidence_manifest.append(dict(source=source_name, archive=archived_name,
                                      sha256=digest(archived), size=len(archived)))
    (CASE / "verification/generation_evidence/manifest.json").write_text(
        json.dumps(evidence_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    for label, valid in checks.items():
        if not valid:
            errors.append(label)
    result = dict(
        instance_id=CONFIG["instance_id"], validated_at_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks, errors=errors, passed=not errors, docker_executed=False,
    )
    (CASE / "verification/layout_validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    summary_path = CASE / "verification/final_summary.json"
    summary = load(summary_path)
    summary["layout_validated"] = not errors
    summary["patch_application_validated"] = checks.get("gold_applies_to_exact_fix_blobs", False)
    summary["checksum_validated"] = "Checksum manifest differs from file contents" not in errors
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
