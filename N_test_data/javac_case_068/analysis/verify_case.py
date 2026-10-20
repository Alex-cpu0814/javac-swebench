"""Verify case 068 record consistency and the local Base/Fix/tamper evidence."""
import json
from pathlib import Path
import subprocess


CASE = Path(__file__).resolve().parents[1]
BASE = "2c007161cff7ba12023ae48dd28a7856c0c6da3d"
FIX = "1ae772163cf3eb432cf6f327db5bf5b7fe9aad5f"
F2P = "org.lwjgl.openvr.VRCompositorNullGamePoseTest::nullGamePose"
P2P = "org.lwjgl.openvr.VRCompositorNullGamePoseTest::nonNullGamePose"


def read_json(name):
    return json.loads((CASE / name).read_text(encoding="utf-8"))


instance = read_json("official_swebench/instance_068.json")
public = read_json("official_swebench/public_task_068.json")
metadata = read_json("official_swebench/metadata.json")
config = read_json("evaluator/case_config.json")
publication_audit = read_json("verification/publication/registry_audit.json")
assert instance["base_commit"] == public["base_commit"] == config["base_commit"] == BASE
assert config["fix_commit"] == metadata["fix_commit"] == FIX
assert instance["patch"] == (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8")
assert instance["test_patch"] == (CASE / "patches/test_patch.diff").read_text(encoding="utf-8")
assert instance["FAIL_TO_PASS"] == config["FAIL_TO_PASS"] == [F2P]
assert instance["PASS_TO_PASS"] == config["PASS_TO_PASS"] == [P2P]
assert all(instance[key] == value for key, value in public.items())
jsonl = (CASE / "official_swebench/instance_068.jsonl").read_text(encoding="utf-8").splitlines()
assert len(jsonl) == 1 and json.loads(jsonl[0]) == instance

source = CASE.parents[2] / "_work/lwjgl3-100"
if (source / ".git").exists():
    upstream = subprocess.check_output(
        ["git", "-C", str(source), "diff", "--binary", BASE, FIX])
    assert upstream == (CASE / "patches/gold_patch.diff").read_bytes()

build = read_json("verification/builds/case-068-build-final/summary.json")
base = read_json("verification/runs/case-068-base-final/summary.json")
base_grading = read_json("verification/runs/case-068-base-final/grading.json")
gold = read_json("verification/runs/case-068-gold-final/summary.json")
gold_grading = read_json("verification/runs/case-068-gold-final/grading.json")
tamper = read_json("verification/runs/case-068-tamper-final/summary.json")
assert build["status"] == "success" and build["clean_base_verified"]
assert build["fix_object_absent"] and build["protected_tests_absent"]
assert build["project_binaries_absent"]
assert base["status"] == "unresolved" and base_grading["FAIL_TO_PASS"][F2P] == "FAILED"
assert base_grading["PASS_TO_PASS"][P2P] == "PASSED"
assert gold["status"] == "resolved" and gold_grading["FAIL_TO_PASS"][F2P] == "PASSED"
assert gold_grading["PASS_TO_PASS"][P2P] == "PASSED"
assert tamper["status"] == "unresolved" and tamper["reason"] == "candidate_conflicts_with_test_patch"
assert build["image_id"] == base["image"]["id"] == gold["image"]["id"]
assert metadata["verification"]["image_id"] == build["image_id"]
assert metadata["status"] == "published_completed"
assert metadata["publication"]["digest"] == build["image_id"] == publication_audit["digest"]
assert config["image"] == metadata["publication"]["image"].split(":benchmark-v1")[0] + "@" + publication_audit["digest"]
assert publication_audit["anonymous_registry_manifest_status"] == 200
assert publication_audit["digest_pull_succeeded"] and publication_audit["network_disabled_during_image_audit"]
assert "calls=0" in (CASE / "verification/runs/case-068-base-final/nullGamePose.private.log").read_text(encoding="utf-8")
assert "gameAddress=0 gameCount=0" in (CASE / "verification/runs/case-068-gold-final/nullGamePose.private.log").read_text(encoding="utf-8")

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
print("Case 068 records and local controls verified")
