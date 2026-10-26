"""Validate the renumbered real JNI case and reject no-op closes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

CASE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suffix", default="lifecycle-final")
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--docker", default="docker")
    args = parser.parse_args()
    if not args.suffix.replace("-", "").isalnum():
        raise SystemExit("Invalid suffix")
    digest = hashlib.sha256((CASE / "patches/test_patch.diff").read_bytes()).hexdigest()
    instance = json.loads((CASE / "official_swebench/instance_097.json").read_text(encoding="utf-8"))
    synthetic = {"test_close_lifecycle.TestCloseLifecycle.test_same_thread_close",
                 "test_close_lifecycle.TestCloseLifecycle.test_double_close"}
    scenarios = (("gold", "patches/gold_patch.diff", 0),
                 ("base", "verification/controls/negative_patch.diff", 1),
                 ("close-noop", "verification/controls/close_noop.patch", 1),
                 ("close-flag-only", "verification/controls/close_flag_only.patch", 1),
                 ("tamper", "verification/controls/test_tamper.patch", 1))
    runs = {}
    for label, patch, expected_exit in scenarios:
        run_id = "case-097-" + label + "-" + args.suffix
        directory = CASE / "verification/runs" / run_id
        summary_path = directory / "summary.json"
        if not (args.reuse_existing and summary_path.is_file()):
            result = subprocess.run([sys.executable, str(CASE / "evaluator/evaluate_model_patch.py"),
                "--patch", str(CASE / patch), "--run-id", run_id, "--timeout", "300", "--docker", args.docker])
            assert result.returncode == expected_exit, (label, result.returncode)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        assert summary["test_patch_sha256"] == digest
        assert summary["model_patch_sha256"] == hashlib.sha256((CASE / patch).read_bytes()).hexdigest()
        if label == "tamper":
            assert summary["reason"] == "candidate_conflicts_with_test_patch"
        else:
            grading = json.loads((directory / "grading.json").read_text())
            f2p = "PASSED" if label == "gold" else "FAILED"
            assert grading["FAIL_TO_PASS"] == {name: f2p for name in instance["FAIL_TO_PASS"]}
            assert grading["PASS_TO_PASS"] == {
                name: "FAILED" if label in ("close-noop", "close-flag-only") and name in synthetic else "PASSED"
                for name in instance["PASS_TO_PASS"]}, (label, grading)
            assert grading["tests_observed"] == 81
            child = (directory / "children/terminated-thread.log").read_text()
            if label == "gold":
                assert all(marker in child for marker in ("CLOSE_OK", "CLOSE_STEP:0", "CLOSE_STEP:1", "CLOSE_STEP:2"))
            elif label == "base":
                assert "CLOSING:0" in child and "SIGSEGV" in child
            else:
                assert "Python sub-interpreter was not torn down exactly once" in child
        runs[label] = run_id
    report = {"case_number": "097", "instance_id": instance["instance_id"],
              "previous_case_number": "096", "test_patch_sha256": digest, "runs": runs,
              "base_fails": True, "fix_passes": True, "PASS_TO_PASS_COUNT": 80,
              "same_thread_close_verified": True, "double_close_verified": True,
              "native_teardown_verified": True, "no_op_close_rejected": True,
              "flag_only_close_rejected": True, "test_tamper_rejected": True}
    (CASE / "verification/local_evidence.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
