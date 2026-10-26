"""Freeze the verified 096-to-097 migration and current lifecycle controls."""
import hashlib
import json
import os
from pathlib import Path

CASE = Path(__file__).resolve().parents[1]
OFFICIAL = CASE / "official_swebench"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def release_files():
    for path in sorted(CASE.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.name.endswith(".local.json") or path.name == "SHA256SUMS.txt":
            continue
        if "case-097-gold-lifecycle-check" in path.parts:
            continue
        yield path


def main():
    evidence = read(CASE / "verification/local_evidence.json")
    digest = hashlib.sha256((CASE / "patches/test_patch.diff").read_bytes()).hexdigest()
    assert evidence["test_patch_sha256"] == digest and evidence["fix_passes"]
    docker = read(CASE / "verification/docker_publication.json")
    assert docker["anonymous_http_status"] == 200 and docker["digest_pull_verified"]
    smoke = read(CASE / "verification/runs/case-097-gold-published-digest/summary.json")
    assert smoke["status"] == "resolved" and smoke["test_patch_sha256"] == digest
    audit = read(CASE / "verification/builds/case-097-retag-audit/summary.json")
    assert audit["clean_base_verified"] and audit["fix_object_absent"] and audit["protected_tests_absent"]
    evidence["published_digest_smoke_run_id"] = smoke["run_id"]
    evidence["image"] = docker["image"]
    write(CASE / "verification/local_evidence.json", evidence)
    instance = read(OFFICIAL / "instance_097.json")
    instance["patch"] = (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8")
    instance["test_patch"] = (CASE / "patches/test_patch.diff").read_text(encoding="utf-8")
    write(OFFICIAL / "instance_097.json", instance)
    (OFFICIAL / "instance_097.jsonl").write_text(json.dumps(instance, ensure_ascii=False, separators=(",", ":")) + "\n",
                                               encoding="utf-8", newline="\n")
    metadata = read(OFFICIAL / "metadata.json")
    metadata["verification"].update({
        "status": "resolved", "base_fails": True, "fix_passes": True, "docker_verified": True,
        "test_patch_sha256": digest, "model_evaluator_verified": True,
        "PASS_TO_PASS_COUNT": 80, "same_thread_close_verified": True, "double_close_verified": True,
        "native_teardown_verified": True, "no_op_close_rejected": True, "flag_only_close_rejected": True,
        "base_run_id": evidence["runs"]["base"], "gold_run_id": evidence["runs"]["gold"],
        "test_tamper_rejected": True, "published_digest_smoke_run_id": smoke["run_id"],
    })
    metadata["patch_provenance"].update(official_diff_complete=True, changed_file_count=6)
    metadata["model_evaluator_image"] = docker["image"]
    metadata["previous_case_number"] = "096"
    metadata["publication"] = {"github_repository": "https://github.com/Alex-cpu0814/javac-swebench",
        "github_case_path": "N_test_data/javac_case_097", "docker_repository": docker["repository"],
        "docker_digest": docker["digest"], "docker_publication_verified": True}
    metadata["notes"] = ["Original issue #22 reports Linux/amd64, not a Windows-only defect.",
        "Specific stale-JNIEnv close crash reproduced on Linux, Java 8 and Python 3.4.10; arbitrary cross-thread access remains unsafe.",
        "81 formal tests: 1 synthetic F2P, 78 existing upstream P2P, 2 synthetic lifecycle P2P.",
        "Old 096 raw logs retain original identifiers; current verification and publication use 097."]
    write(OFFICIAL / "metadata.json", metadata)
    environment = read(CASE / "analysis/environment_spec.json")
    environment["verification"].update(metadata["verification"])
    environment["reproduction_status"] = "resolved"
    environment["notes"] = metadata["notes"]
    write(CASE / "analysis/environment_spec.json", environment)
    row = read(CASE / "analysis/source_row_097.json")
    row["verification_status"] = "resolved"
    row["pass_to_pass_count"] = 80
    row["test_strategy"] = "Bounded child JVM; terminated creator; completion protocol; real Python teardown marker; same-thread and repeated close controls"
    write(CASE / "analysis/source_row_097.json", row)
    checks = []
    for path in release_files():
        name = os.path.relpath(path, OFFICIAL).replace("\\", "/")
        checks.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + name)
    (OFFICIAL / "SHA256SUMS.txt").write_text("\n".join(checks) + "\n", encoding="ascii", newline="\n")
    print("Frozen case 097:", len(checks), "checksum entries")


if __name__ == "__main__":
    main()
