"""Regenerate SWE-bench records, protected patch, and checksums from pinned inputs."""
import hashlib
import json
from pathlib import Path


CASE = Path(__file__).resolve().parents[1]
OFFICIAL = CASE / "official_swebench"
TEST_ASSETS = {
    "PointerBuffer.java": "config/tests/case074/org/lwjgl/PointerBuffer.java",
    "MemoryAccess.java": "config/tests/case074/org/lwjgl/system/MemoryAccess.java",
    "MemoryUtil.java": "config/tests/case074/org/lwjgl/system/MemoryUtil.java",
    "AllocatorProbe.java": "config/tests/case074/org/lwjgl/system/AllocatorProbe.java",
    "PointerInitializationProbe.java": "config/tests/case074/org/lwjgl/system/PointerInitializationProbe.java",
    "pointer_size.c": "config/tests/case074/pointer_size.c",
    "jemalloc_stub.c": "config/tests/case074/jemalloc_stub.c",
}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


parts = []
for source, target in TEST_ASSETS.items():
    content = (CASE / "patches" / source).read_text(encoding="utf-8").replace("\r\n", "\n")
    assert content.endswith("\n"), source
    lines = content.splitlines()
    parts += [f"diff --git a/{target} b/{target}", "new file mode 100644", "--- /dev/null",
              f"+++ b/{target}", f"@@ -0,0 +1,{len(lines)} @@"]
    parts += ["+" + line for line in lines]
(CASE / "patches/test_patch.diff").write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")

row = json.loads((CASE / "analysis/source_row_074.json").read_text(encoding="utf-8"))
public = {
    "instance_id": row["instance_id"],
    "repo": row["repo"],
    "base_commit": row["base_commit"],
    "problem_statement": row["problem_statement"],
    "hints_text": None,
    "created_at": "2015-11-13",
    "version": "3.0.0b",
}
instance = {
    **public,
    "patch": (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8"),
    "test_patch": (CASE / "patches/test_patch.diff").read_text(encoding="utf-8"),
    "FAIL_TO_PASS": row["FAIL_TO_PASS"],
    "PASS_TO_PASS": row["PASS_TO_PASS"],
}
write_json(OFFICIAL / "public_task_074.json", public)
write_json(OFFICIAL / "instance_074.json", instance)
(OFFICIAL / "instance_074.jsonl").write_text(
    json.dumps(instance, ensure_ascii=False, separators=(",", ":")) + "\n",
    encoding="utf-8", newline="\n")

paths = [
    "instance_074.json", "instance_074.jsonl", "public_task_074.json", "metadata.json",
    "../patches/gold_patch.diff", "../patches/test_patch.diff",
    *["../patches/" + name for name in TEST_ASSETS],
    "../analysis/source_row_074.json", "../analysis/environment_spec.json",
    "../analysis/verify_case.py",
    "../evaluator/case_config.json", "../evaluator/build_model_evaluator.py",
    "../evaluator/evaluate_model_patch.py", "../evaluator/build_project.py",
    "../evaluator/test_runner.py", "../evaluator/logging_v3.py",
    "../evaluator/run_evaluation.sh",
    "../evaluator/case_adapter.sh", "../evaluator/image/Dockerfile",
    "../verification/local_evidence.json",
    "../verification/publication/registry_audit.json",
    "../verification/builds/case-074-build-final/summary.json",
    "../verification/runs/case-074-base-final/summary.json",
    "../verification/runs/case-074-base-final/grading.json",
    "../verification/runs/case-074-gold-final/summary.json",
    "../verification/runs/case-074-gold-final/grading.json",
    "../verification/runs/case-074-tamper-final/summary.json",
    "../verification/runs/case-074-tamper-final/grading.json",
    "../verification/controls/base_control.patch",
    "../verification/controls/test_tamper.patch",
    "../verification/focused_reproduction/compare.log",
    "../verification/focused_reproduction/source_manifest.json",
]
lines = []
for name in paths:
    path = OFFICIAL / name
    if path.is_file():
        lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + name)
(OFFICIAL / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
print("Generated instance, public task, JSONL, protected patch and", len(lines), "checksums")
