from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "Y_test_data" / "javac_case_112"
OFFICIAL = CASE / "official_swebench"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


gold_patch = (CASE / "patches" / "gold_patch.diff").read_text(encoding="utf-8")
test_patch = (CASE / "patches" / "test_patch.diff").read_text(encoding="utf-8")

instance = {
    "version": "2.1.0",
    "test_patch": test_patch,
    "hints_text": None,
    "problem_statement": (
        "OpenJPEG lossless compression is not bit-exact on 32-bit Linux/x86. "
        "Compressing issue571.tif with the default lossless settings and then "
        "decoding it produces a TIFF whose pixels differ from the input. The "
        "lossless round trip must preserve every image component exactly."
    ),
    "FAIL_TO_PASS": ["openjpeg.issue571.lossless_roundtrip"],
    "patch": gold_patch,
    "base_commit": "4f5ec07c315872bdee0885be085ebf57cede2db9",
    "instance_id": "uclouvain__openjpeg-571",
    "repo": "uclouvain/openjpeg",
    "created_at": "2015-09-01",
    "issue_id": 571,
    "issue_url": "https://github.com/uclouvain/openjpeg/issues/571",
    "pull_request_id": 579,
    "pull_request_url": "https://github.com/uclouvain/openjpeg/pull/579",
    "PASS_TO_PASS": [
        "openjpeg.issue571.encode_issue571",
        "openjpeg.issue571.decode_issue571",
    ],
    "fix_commit": "5d953558de8dc4d939b8147fe9547533a8804297",
    "test_files": [
        "tests/compare_images.c",
        "tests/nonregression/CMakeLists.txt",
        "tests/nonregression/test_suite.ctest.in",
    ],
    "test_command": (
        "cmake -S . -B /opt/openjpeg-build -DBUILD_TESTING=ON "
        "-DBUILD_THIRDPARTY=ON -DOPJ_DATA_ROOT=/opt/openjpeg-data; "
        "cmake --build /opt/openjpeg-build; "
        "opj_compress issue571.tif; opj_decompress issue571.tif.j2k; "
        "compare_images issue571.tif issue571.lossless.tif"
    ),
}

metadata = {
    "dataset_schema_version": "1.0",
    "source_case": "112",
    "dataset_variant": "SWE-bench-compatible custom record",
    "test_source": "official_upstream_regression_test",
    "created_at_source": (
        "GitHub API for OpenJPEG issue #571, pull request #579, and upstream "
        "merge commit 5d953558de8dc4d939b8147fe9547533a8804297"
    ),
    "PASS_TO_PASS_COUNT": len(instance["PASS_TO_PASS"]),
    "created_at": instance["created_at"],
    "FAIL_TO_PASS": instance["FAIL_TO_PASS"],
    "version": instance["version"],
    "issue_url": instance["issue_url"],
    "PASS_TO_PASS": instance["PASS_TO_PASS"],
    "standard_layout": {
        "schema_version": "2.0",
        "case_directory": "javac_case_112",
        "analysis": "analysis/",
        "patches": "patches/",
        "official_swebench": "official_swebench/",
        "evaluator": "evaluator/",
        "verification": "verification/",
    },
    "verification": {
        "docker_verified": True,
        "model_evaluator_verified": True,
        "fix_passes": True,
        "base_fails": True,
        "model_evaluator_verification_type": "isolated_runtime_injection_32bit_x86_lossless_roundtrip",
        "evaluation_assets_injected_at_runtime": True,
        "image_contains_test_patch": False,
        "image_contains_gold_patch": False,
        "image_contains_fix_commit": False,
        "template_version": "1.0",
        "image_build_id": "case-112-build-2",
        "image": "javac-case-112-openjpeg:benchmark-v1",
        "image_id": "sha256:33a22445240b5d6abba03d5c41a277d721fc8940f51aa3e7b7138daeb2f87305",
        "gold_run_id": "case-112-gold-1",
        "base_run_id": "case-112-base-1",
        "gold_grading": {
            "FAIL_TO_PASS": {"passed": 1, "expected": 1},
            "PASS_TO_PASS": {"passed": 2, "expected": 2},
            "unexpected_failures": 0,
        },
        "base_grading": {
            "FAIL_TO_PASS": {"failed": 1, "expected": 1},
            "PASS_TO_PASS": {"passed": 2, "expected": 2},
            "unexpected_failures": 1,
            "different_pixels": 19,
            "maximum_component_error": 3,
        },
    },
    "test_command": instance["test_command"],
    "base_commit": instance["base_commit"],
    "repo": instance["repo"],
    "patch_provenance": {
        "gold_patch_authorship": "uclouvain/openjpeg_upstream",
        "gold_patch_source": "official_upstream_fix_commit",
        "test_patch_source": "official_upstream_regression_test",
        "test_patch_authorship": "uclouvain/openjpeg_upstream",
        "upstream_regression_test_found": True,
        "test_data_source": "uclouvain/openjpeg-data@68b30b7f390b852106fb5ee2cf1dbc8628a2feaf",
        "test_data_sha256": "1c9dcd1801aac971759da985661bf074beb4c3a19c6ac4dbd8a0775f7f018e44",
        "model_patch_example_source": "copy_of_gold_patch_for_evaluator_smoke_test",
        "model_patch_example_is_model_generated": False,
    },
    "fix_commit": instance["fix_commit"],
    "instance_id": instance["instance_id"],
    "issue_id": instance["issue_id"],
    "pull_request_id": instance["pull_request_id"],
    "test_files": instance["test_files"],
    "project_version": instance["version"],
    "model_evaluator_image": "javac-case-112-openjpeg:benchmark-v1",
    "published_image": "yutu0814/javac-case-112-openjpeg:benchmark-v1",
    "published_image_digest": "sha256:33a22445240b5d6abba03d5c41a277d721fc8940f51aa3e7b7138daeb2f87305",
    "docker_hub_url": "https://hub.docker.com/r/yutu0814/javac-case-112-openjpeg",
    "FAIL_TO_PASS_COUNT": len(instance["FAIL_TO_PASS"]),
    "notes": [
        "Source spreadsheet row: deduplicated Java-C sequence 112 (original row 113).",
        "The regression is architecture-sensitive and is evaluated with GCC -m32 on Linux/x86.",
        "The official issue571.tif input is pinned by repository commit and SHA-256.",
    ],
}

source_row = {
    "instance_id": instance["instance_id"],
    "source_project": "Dissecting Real-World Cross-Language Bugs",
    "source_case": "112",
    "source_workbook_sequence": 112,
    "source_workbook_original_row": 113,
    "language_pair": "Java-C",
    "repo": instance["repo"],
    "issue_id": instance["issue_id"],
    "issue_url": instance["issue_url"],
    "pull_request_id": instance["pull_request_id"],
    "pull_request_url": instance["pull_request_url"],
    "commit": instance["fix_commit"],
    "base_commit": instance["base_commit"],
    "base_commit_status": "verified_first_parent_of_merge_commit",
    "fix_commit": instance["fix_commit"],
    "commit_url": f"https://github.com/{instance['repo']}/commit/{instance['fix_commit']}",
    "problem_statement": instance["problem_statement"],
    "symptom": "lossless encoding produces a non-identical decoded image on 32-bit x86",
    "root_cause": "floating-point comparison logic error",
    "fixing_strategy": "compare the rate-distortion threshold using a DBL_EPSILON margin",
    "evidence_type": "official_issue_pull_request_and_regression_test",
    "test_source": metadata["test_source"],
    "test_files": instance["test_files"],
    "verification_status": "resolved",
    "FAIL_TO_PASS": instance["FAIL_TO_PASS"],
    "PASS_TO_PASS_COUNT": len(instance["PASS_TO_PASS"]),
}

environment = {
    "instance_id": instance["instance_id"],
    "task_level": "integration",
    "validation_type": "official_project_lossless_roundtrip",
    "environment": "Debian Bookworm Linux container using a 32-bit x86 GCC target",
    "python_version_target": "3.11 (evaluator orchestration only)",
    "java_requirement": "default JDK (dataset compatibility/audit only; not used by the regression)",
    "native_requirement": "GCC multilib with -m32; bundled zlib/libpng/libtiff/lcms2",
    "build_system": "CMake at the verified Base commit",
    "test_execution": instance["test_command"],
    "runtime_verified": True,
    "notes": [
        "The upstream issue reports the defect on Linux x86 (-m32).",
        "The official test input is fetched from the historical openjpeg-data merge commit 68b30b7f390b852106fb5ee2cf1dbc8628a2feaf.",
        "Base control: encode/decode pass, but 19 pixels differ and the lossless comparison fails.",
        "Gold control: all three expected tests pass with no unexpected failures.",
    ],
    "reproduction_status": "verified_base_fail_fix_pass_docker",
    "base_commit": instance["base_commit"],
    "fix_commit": instance["fix_commit"],
    "test_source": metadata["test_source"],
    "test_files": instance["test_files"],
    "FAIL_TO_PASS": instance["FAIL_TO_PASS"],
    "PASS_TO_PASS_COUNT": len(instance["PASS_TO_PASS"]),
    "verification": metadata["verification"],
}

write_json(OFFICIAL / "instance_112.json", instance)
write_json(OFFICIAL / "metadata.json", metadata)
write_json(CASE / "analysis" / "source_row_112.json", source_row)
write_json(CASE / "analysis" / "environment_spec.json", environment)

(CASE / "README.md").write_text(
    """# Java-C SWE-bench Case 112

This case is derived from OpenJPEG merge commit
`5d953558de8dc4d939b8147fe9547533a8804297`, which fixes Issue #571: a
supposedly lossless JPEG 2000 round trip changes pixels on 32-bit Linux/x86.

## Identity

- Instance: `uclouvain__openjpeg-571`
- Repository: `uclouvain/openjpeg`
- Base: `4f5ec07c315872bdee0885be085ebf57cede2db9`
- Fix: `5d953558de8dc4d939b8147fe9547533a8804297`
- Issue: [#571](https://github.com/uclouvain/openjpeg/issues/571)
- Pull request: [#579](https://github.com/uclouvain/openjpeg/pull/579)
- Source spreadsheet sequence: `112`

## Test and environment

The protected patch is the exact upstream regression-test portion of the fix.
The evaluator builds the Base as 32-bit x86 with GCC, runs the official
`issue571.tif` lossless encode/decode sequence, and compares every component
with the upstream `compare_images` utility. The input file is pinned to the
historical `openjpeg-data` commit and verified by SHA-256.

## Published evaluator image

`yutu0814/javac-case-112-openjpeg:benchmark-v1`

Digest: `sha256:33a22445240b5d6abba03d5c41a277d721fc8940f51aa3e7b7138daeb2f87305`
""",
    encoding="utf-8",
    newline="\n",
)

(CASE / "analysis" / "README.md").write_text(
    """# Case 112 analysis

OpenJPEG Issue #571 reports that default lossless compression fails on Linux
x86 while the same input succeeds on x86-64. Pull request #579 adds the
`issue571.tif` regression input and an encode/decode/component-comparison test.
The production change is isolated in `src/lib/openjp2/tcd.c`; all upstream test
harness changes are isolated in `patches/test_patch.diff`.
""",
    encoding="utf-8",
    newline="\n",
)
