"""Local, targeted Java-struct evaluation; requires the preserved experiment workspace."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile


CASE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((CASE / "evaluator/case_config.json").read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def apply_patch(source: Path, patch: Path, log: Path) -> None:
    if not patch.read_bytes().strip():
        log.write_text("Empty patch: no production change.\n", encoding="utf-8")
        return
    with log.open("wb") as output:
        for options in (["--check"], []):
            subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(source), "apply", *options, str(patch)],
                           check=True, stdout=output, stderr=subprocess.STDOUT)


def export_base(repo: Path, source: Path) -> None:
    archive = subprocess.check_output(["git", "-C", str(repo), "archive", CONFIG["base_commit"]])
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        # Source is trusted pinned upstream Git content. Also reject escaping entries/links.
        root = source.resolve()
        for member in tar.getmembers():
            target = (source / member.name).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"Archive path escapes source tree: {member.name}")
            if member.issym() or member.islnk():
                raise ValueError(f"Unexpected link in source archive: {member.name}")
        tar.extractall(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--revision", choices=["base", "fix"], default=None)
    selection.add_argument("--patch", type=Path)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--image", default=CONFIG["image"])
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    work = (args.workspace or CASE / CONFIG["experiment_workspace"]).resolve()
    run_id = "case-056-local-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    output = CASE / "verification/runs" / run_id
    output.mkdir(parents=True)
    summary = dict(instance_id=CONFIG["instance_id"], run_id=run_id,
                   status="error", mode=args.revision or ("candidate" if args.patch else "base"),
                   scope="targeted_struct_recompile_reusing_base_binary_dependencies",
                   formal_evaluator=False, tests={}, image=args.image)
    exit_code = 2
    try:
        for rel in [
            "lwjgl3-parent/bin/classes/lwjgl/core/org/lwjgl/system/MemoryStack.class",
            "lwjgl3-parent/bin/classes/lwjgl/vulkan/org/lwjgl/vulkan/VkFramebufferCreateInfo.class",
            "lwjgl3-parent/bin/libs/java/jsr305.jar", "lwjgl3-parent/bin/libs/java/testng.jar",
            "lwjgl3-parent/bin/libs/java/jcommander.jar",
            "runtime/lwjgl-native/linux/x64/org/lwjgl/liblwjgl.so",
        ]:
            if not (work / rel).is_file():
                raise FileNotFoundError(f"Required local dependency missing: {work / rel}")
        repo = work / "lwjgl3-parent"
        test_patch = CASE / "patches/test_patch.diff"
        if args.patch:
            candidate = args.patch.resolve()
        elif args.revision == "fix":
            candidate = CASE / "patches/gold_patch.diff"
        else:
            candidate = None
        summary["candidate_patch_sha256"] = sha(candidate.read_bytes()) if candidate else None
        summary["test_patch_sha256"] = sha(test_patch.read_bytes())
        with tempfile.TemporaryDirectory(prefix="case056-") as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            export_base(repo, source)
            if candidate:
                # Disallow candidate edits to protected test and runner locations.
                text = candidate.read_text(encoding="utf-8-sig")
                for line in text.splitlines():
                    if line.startswith(("+++ ", "--- ", "rename to ", "rename from ")):
                        if "/src/test/" in line or "RunVkFramebufferCreateInfoTests" in line:
                            raise ValueError("candidate_conflicts_with_test_patch")
                apply_patch(source, candidate, output / "model-patch.raw.log")
            if (source / CONFIG["test_file"]).exists():
                raise ValueError("candidate_conflicts_with_test_patch")
            apply_patch(source, test_patch, output / "test-patch.raw.log")
            summary["target_source_sha256"] = sha((source / CONFIG["source_file"]).read_bytes())
            summary["test_source_sha256"] = sha((source / CONFIG["test_file"]).read_bytes())
            command = [
                "docker", "run", "--rm", "--network", "none",
                "--mount", f"type=bind,source={source},target=/source,readonly",
                "--mount", f"type=bind,source={work},target=/support,readonly",
                "--mount", f"type=bind,source={CASE / 'evaluator'},target=/benchmark,readonly",
                "--mount", f"type=bind,source={output},target=/results",
                args.image, "bash", "/benchmark/run_evaluation.sh",
            ]
            with (output / "docker-run.stdout.raw.log").open("wb") as stdout, \
                    (output / "docker-run.stderr.raw.log").open("wb") as stderr:
                result = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=args.timeout)
            summary["docker_exit_code"] = result.returncode
        log_path = output / "tests.raw.log"
        if not log_path.exists():
            raise RuntimeError("Tests did not start; inspect compilation.raw.log / Docker logs")
        text = log_path.read_text(encoding="utf-8", errors="replace")
        found = re.findall(r"^(PASS|FAIL): (test\w+)$", text, flags=re.MULTILINE)
        expected = [node.rsplit("::", 1)[1] for node in CONFIG["FAIL_TO_PASS"]]
        if len(found) != len(expected) or sorted(name for _, name in found) != sorted(expected):
            raise RuntimeError("Missing, duplicate or unexpected test results")
        summary["tests"] = {name: status.lower() for status, name in found}
        failed = sum(status == "FAIL" for status, _ in found)
        if result.returncode != (1 if failed else 0):
            raise RuntimeError("Docker exit code disagrees with observed test results")
        summary.update(status="unresolved" if failed else "resolved", passed=2 - failed, failed=failed)
        exit_code = 1 if failed else 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        summary["error"] = str(error)
    summary["exit_code"] = exit_code
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Results: {output}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
