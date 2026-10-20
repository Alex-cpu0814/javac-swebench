"""Verify case 074 records and Base/Fix/tamper evidence."""
import hashlib
import json
from pathlib import Path
import subprocess


CASE = Path(__file__).resolve().parents[1]
BASE = "1fa5a394949cad836a104d8e5093f734d26ff8e1"
FIX = "4fb6618bfd8990b8a0b805f589a76ff4a1b56684"
F2P = "org.lwjgl.system.PointerInitializationProbe::allocatorSelection"
P2P = "org.lwjgl.system.PointerInitializationProbe::pointerWidth"


def read_json(name):
    return json.loads((CASE / name).read_text(encoding="utf-8"))


instance = read_json("official_swebench/instance_074.json")
public = read_json("official_swebench/public_task_074.json")
metadata = read_json("official_swebench/metadata.json")
config = read_json("evaluator/case_config.json")
assert instance["base_commit"] == public["base_commit"] == config["base_commit"] == BASE
assert config["fix_commit"] == metadata["fix_commit"] == FIX
assert instance["patch"] == (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8")
assert instance["test_patch"] == (CASE / "patches/test_patch.diff").read_text(encoding="utf-8")
assert instance["FAIL_TO_PASS"] == config["FAIL_TO_PASS"] == [F2P]
assert instance["PASS_TO_PASS"] == config["PASS_TO_PASS"] == [P2P]
assert all(instance[key] == value for key, value in public.items())
jsonl = (CASE / "official_swebench/instance_074.jsonl").read_text(encoding="utf-8").splitlines()
assert len(jsonl) == 1 and json.loads(jsonl[0]) == instance

source = CASE.parents[2] / "_work/lwjgl3-100"
if (source / ".git").exists():
    parent = subprocess.check_output(["git", "-C", str(source), "rev-parse", FIX + "^"])
    assert parent.decode().strip() == BASE
    diff = subprocess.check_output(["git", "-C", str(source), "diff", "--binary", BASE, FIX])
    assert diff == (CASE / "patches/gold_patch.diff").read_bytes()
    changed = subprocess.check_output(["git", "-C", str(source), "diff", "--name-only", BASE, FIX])
    assert len(changed.splitlines()) == metadata["patch_provenance"]["changed_file_count"] == 5
    manifest = read_json("verification/focused_reproduction/source_manifest.json")
    pointer = "modules/core/src/main/java/org/lwjgl/system/Pointer.java"
    for variant, commit in (("base", BASE), ("fixed", FIX)):
        upstream = subprocess.check_output(["git", "-C", str(source), "show", commit + ":" + pointer])
        assert hashlib.sha256(upstream).hexdigest() == manifest["files"][variant]["sha256"]

build = read_json("verification/builds/case-074-build-final/summary.json")
base = read_json("verification/runs/case-074-base-final/summary.json")
base_grading = read_json("verification/runs/case-074-base-final/grading.json")
gold = read_json("verification/runs/case-074-gold-final/summary.json")
gold_grading = read_json("verification/runs/case-074-gold-final/grading.json")
tamper = read_json("verification/runs/case-074-tamper-final/summary.json")
assert build["status"] == "success" and build["clean_base_verified"]
assert build["fix_object_absent"] and build["protected_tests_absent"]
assert build["project_binaries_absent"]
assert base["status"] == "unresolved" and base["phase"]["phase"] == "tests_complete"
assert base_grading["FAIL_TO_PASS"][F2P] == "FAILED"
assert base_grading["PASS_TO_PASS"][P2P] == "PASSED"
assert gold["status"] == "resolved" and gold_grading["FAIL_TO_PASS"][F2P] == "PASSED"
assert gold_grading["PASS_TO_PASS"][P2P] == "PASSED"
assert tamper["status"] == "unresolved" and tamper["reason"] == "candidate_conflicts_with_test_patch"
assert build["image_id"] == base["image"]["id"] == gold["image"]["id"]
assert config["image_id"] == metadata["verification"]["image_id"] == build["image_id"]
base_log = (CASE / "verification/runs/case-074-base-final/allocatorSelection.private.log").read_text(encoding="utf-8")
gold_log = (CASE / "verification/runs/case-074-gold-final/allocatorSelection.private.log").read_text(encoding="utf-8")
assert "attempted_library=libjemalloc32.so loaded=false" in base_log
assert "pointer_size=8 bits64=true" in base_log
assert "attempted_library=libjemalloc.so loaded=true" in gold_log
assert "pointer_size=8 bits64=true" in gold_log
assert metadata["status"] == "published_completed"
publication = metadata["publication"]
audit = read_json("verification/publication/registry_audit.json")
assert publication["status"] == "published_completed"
assert all(publication[key] for key in (
    "image_published", "github_published", "registry_pull_verified",
    "registry_public_access_verified", "published_image_audit_passed"))
assert audit["image"] == publication["image"]
assert audit["digest"] == publication["digest"]
assert config["image"] == publication["image"].split(":benchmark-v1")[0] + "@" + audit["digest"]
assert audit["digest"] == build["image_id"]
assert audit["anonymous_registry_manifest_status"] == 200
assert all(audit[key] for key in (
    "digest_pull_succeeded", "working_tree_clean", "protected_test_absent",
    "fix_commit_object_absent", "network_disabled_during_image_audit"))
assert audit["pinned_base_commit"] == BASE
assert not metadata["verification"]["full_ant_build_verified"]

evidence = {
    "instance_id": instance["instance_id"],
    "base_commit": BASE,
    "fix_commit": FIX,
    "image_id": build["image_id"],
    "clean_base_image_verified": True,
    "official_diff_exact": (source / ".git").exists(),
    "base_grading": base_grading,
    "gold_grading": gold_grading,
    "test_tamper_rejected": True,
    "status": metadata["status"],
}
output = CASE / "verification/local_evidence.json"
output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8", newline="\n")
print("Case 074 records, controls and publication audit verified")
