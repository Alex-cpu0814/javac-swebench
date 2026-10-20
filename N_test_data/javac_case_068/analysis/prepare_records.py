"""Regenerate the SWE-bench records and case checksums from pinned inputs."""
import hashlib
import json
from pathlib import Path


CASE = Path(__file__).resolve().parents[1]
OFFICIAL = CASE / "official_swebench"


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


row = json.loads((CASE / "analysis/source_row_068.json").read_text(encoding="utf-8"))
problem = row["problem_statement"]
public = {
    "instance_id": row["instance_id"],
    "repo": row["repo"],
    "base_commit": row["base_commit"],
    "problem_statement": problem,
    "hints_text": None,
    "created_at": "2018-09-27",
    "version": "3.2.0",
}
instance = {
    **public,
    "patch": (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8"),
    "test_patch": (CASE / "patches/test_patch.diff").read_text(encoding="utf-8"),
    "FAIL_TO_PASS": row["FAIL_TO_PASS"],
    "PASS_TO_PASS": row["PASS_TO_PASS"],
}
write_json(OFFICIAL / "public_task_068.json", public)
write_json(OFFICIAL / "instance_068.json", instance)
(OFFICIAL / "instance_068.jsonl").write_text(
    json.dumps(instance, ensure_ascii=False, separators=(",", ":")) + "\n",
    encoding="utf-8", newline="\n")

paths = [
    "instance_068.json", "instance_068.jsonl", "public_task_068.json", "metadata.json",
    "../patches/gold_patch.diff", "../patches/test_patch.diff",
    "../patches/VRCompositorNullGamePoseTest.java", "../patches/vrprobe.c",
    "../analysis/source_row_068.json", "../analysis/environment_spec.json",
    "../evaluator/case_config.json", "../evaluator/build_model_evaluator.py",
    "../evaluator/evaluate_model_patch.py", "../evaluator/build_project.py",
    "../evaluator/test_runner.py", "../evaluator/run_evaluation.sh",
    "../evaluator/case_adapter.sh", "../evaluator/image/Dockerfile",
    "../verification/local_evidence.json",
    "../verification/publication/registry_audit.json",
    "../verification/builds/case-068-build-final/summary.json",
    "../verification/runs/case-068-base-final/summary.json",
    "../verification/runs/case-068-base-final/grading.json",
    "../verification/runs/case-068-gold-final/summary.json",
    "../verification/runs/case-068-gold-final/grading.json",
    "../verification/runs/case-068-tamper-final/summary.json",
    "../verification/source_overlay_comparison/base.log",
    "../verification/source_overlay_comparison/fixed.log",
]
lines = []
for name in paths:
    path = OFFICIAL / name
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(digest + "  " + name)
(OFFICIAL / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
print("Generated instance, public task, JSONL and", len(lines), "checksums")
