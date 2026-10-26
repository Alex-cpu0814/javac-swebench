"""Validate identity, byte-exact publication data, lifecycle evidence and hashes."""
import hashlib
import json
from pathlib import Path

CASE = Path(__file__).resolve().parents[1]
OFFICIAL = CASE / "official_swebench"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    assert CASE.name == "javac_case_097"
    config = load(CASE / "evaluator/case_config.json")
    metadata = load(OFFICIAL / "metadata.json")
    instance = load(OFFICIAL / "instance_097.json")
    public = load(OFFICIAL / "public_task_097.json")
    row = load(CASE / "analysis/source_row_097.json")
    assert config["case_number"] == row["source_case"] == metadata["source_case"] == "097"
    assert instance == load(OFFICIAL / "instance_097.jsonl")
    assert instance["instance_id"] == public["instance_id"] == "ninia__jep-22"
    assert instance["base_commit"] == config["base_commit"] == public["base_commit"]
    assert not set(public).intersection({"patch", "test_patch", "FAIL_TO_PASS", "PASS_TO_PASS", "fix_commit"})
    assert instance["patch"] == (CASE / "patches/gold_patch.diff").read_text(encoding="utf-8")
    assert instance["test_patch"] == (CASE / "patches/test_patch.diff").read_text(encoding="utf-8")
    assert instance["PASS_TO_PASS"] == metadata["PASS_TO_PASS"] == row["PASS_TO_PASS"]
    assert len(instance["PASS_TO_PASS"]) == metadata["PASS_TO_PASS_COUNT"] == 80
    assert config["image"].startswith("yutu0814/javac-case-097-jep@sha256:")
    evidence = load(CASE / "verification/local_evidence.json")
    digest = hashlib.sha256((CASE / "patches/test_patch.diff").read_bytes()).hexdigest()
    assert evidence["test_patch_sha256"] == metadata["verification"]["test_patch_sha256"] == digest
    synthetic = {name for name in instance["PASS_TO_PASS"] if name.startswith("test_close_lifecycle.")}
    assert len(synthetic) == 2
    for label, run_id in evidence["runs"].items():
        directory = CASE / "verification/runs" / run_id
        summary = load(directory / "summary.json")
        assert summary["test_patch_sha256"] == digest
        if label == "tamper":
            assert summary["reason"] == "candidate_conflicts_with_test_patch"
            continue
        grading = load(directory / "grading.json")
        assert grading["tests_observed"] == 81
        assert grading["FAIL_TO_PASS"] == {name: "PASSED" if label == "gold" else "FAILED" for name in instance["FAIL_TO_PASS"]}
        assert grading["PASS_TO_PASS"] == {name: "FAILED" if label in ("close-noop", "close-flag-only") and name in synthetic else "PASSED"
                                               for name in instance["PASS_TO_PASS"]}
    smoke = load(CASE / "verification/runs" / evidence["published_digest_smoke_run_id"] / "summary.json")
    assert smoke["status"] == "resolved" and smoke["image"]["name"] == config["image"]
    count = 0
    for line in (OFFICIAL / "SHA256SUMS.txt").read_text(encoding="ascii").splitlines():
        expected, name = line.split("  ", 1)
        assert hashlib.sha256((OFFICIAL / name).read_bytes()).hexdigest() == expected, name
        count += 1
    print("Case 097 verified:", count, "checksums, 81 formal tests, scoped controls and digest smoke")


if __name__ == "__main__":
    main()
