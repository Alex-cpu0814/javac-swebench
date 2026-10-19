"""Build and audit a clean pinned Base image with project-declared dependency caches."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

from logging_v3 import EventLogger, new_identifier, utc_now, write_json, write_text

CASE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image")
    parser.add_argument("--repo-url")
    parser.add_argument("--source-repo", type=Path)
    parser.add_argument("--dependency-cache", type=Path)
    parser.add_argument("--build-id")
    parser.add_argument("--timeout", type=int, default=2400)
    args = parser.parse_args()
    config = json.loads((CASE / "evaluator/case_config.json").read_text(encoding="utf-8"))
    image = args.image or config["image"]
    build_id = args.build_id or new_identifier("case-056-build")
    if not build_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in build_id):
        raise SystemExit("Invalid build ID")
    out = CASE / "verification/builds" / build_id
    out.mkdir(parents=True, exist_ok=False)
    logger = EventLogger(out / "events.jsonl", build_id, "INFO")
    result = dict(build_id=build_id, status="error", image={"name": image}, started_at=utc_now(),
                  base_commit=config["base_commit"], instance_id=config["instance_id"])
    base, fix = config["base_commit"], config["fix_commit"]
    try:
        logger.emit("INFO", "preparation", "build.started", "Preparing depth-one Base source")
        workspace = CASE.parent / "java_case_056_new/lwjgl3-parent"
        source = args.source_repo or (workspace if (workspace / ".git").is_dir() else None)
        source_url = str(source.resolve()) if source else (args.repo_url or config["repo_url"])
        cache = args.dependency_cache or (workspace / "bin/libs" if (workspace / "bin/libs").is_dir() else None)
        with tempfile.TemporaryDirectory(prefix="case056-build-") as temporary:
            context = Path(temporary)
            bare = context / "base.git"
            with (out / "source-preparation.raw.log").open("wb") as log:
                subprocess.run(["git", "init", "--bare", str(bare)], check=True, stdout=log, stderr=log)
                subprocess.run(["git", "-c", "protocol.file.allow=always", "--git-dir", str(bare),
                                "fetch", "--no-tags", "--depth=1", source_url, base],
                               check=True, stdout=log, stderr=log, timeout=300)
            (bare / "HEAD").write_text(base + "\n", encoding="ascii")
            (bare / "config").write_text("[core]\nrepositoryformatversion = 0\nfilemode = true\nbare = false\n", encoding="ascii")
            absent = subprocess.run(["git", "--git-dir", str(bare), "cat-file", "-e", fix + "^{commit}"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if absent.returncode == 0:
                raise RuntimeError("Fix object leaked into prepared Base source")
            with tarfile.open(context / "base-git.tar.gz", "w:gz") as archive:
                for name in ("HEAD", "config", "shallow", "objects"):
                    if (bare / name).exists():
                        archive.add(bare / name, arcname=name)
                directory = bare / "refs"
                directory.mkdir(exist_ok=True)
                archive.add(directory, arcname="refs")
            dependencies = []
            with tarfile.open(context / "dependency-cache.tar.gz", "w:gz") as archive:
                if cache:
                    for name in ("java", "kotlinc"):
                        directory = cache / name
                        if directory.is_dir():
                            archive.add(directory, arcname=name)
                            for path in sorted(directory.rglob("*")):
                                if path.is_file():
                                    dependencies.append(dict(path=str(path.relative_to(cache)).replace("\\", "/"),
                                        sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            write_json(out / "dependency-cache-manifest.json", dependencies)
            shutil.copyfile(CASE / "evaluator/image/Dockerfile", context / "Dockerfile")
            write_text(context / ".dockerignore", "*\n!Dockerfile\n!base-git.tar.gz\n!dependency-cache.tar.gz\n")
            command = ["docker", "build", "--progress=plain", "-t", image,
                       "--build-arg", "BASE_COMMIT=" + base,
                       "--build-arg", "INSTANCE_ID=" + config["instance_id"], str(context)]
            logger.emit("INFO", "docker_build", "build.executing", "Running standard Base Ant build in image")
            with (out / "docker-build.stdout.raw.log").open("wb") as stdout, \
                    (out / "docker-build.stderr.raw.log").open("wb") as stderr:
                subprocess.run(command, check=True, stdout=stdout, stderr=stderr, timeout=args.timeout)
        audit = '''set -euo pipefail
test "$(git -C /testbed rev-parse HEAD)" = "{base}"
test -z "$(git -C /testbed status --porcelain)"
test ! -e /testbed/bin/classes
test ! -e /testbed/bin/libs/native/linux/x64/org/lwjgl/liblwjgl.so
test ! -e /testbed/modules/lwjgl/vulkan/src/test/java/org/lwjgl/vulkan/VkFramebufferCreateInfoTest.java
test ! -e /benchmark/run_evaluation.sh
test ! -e /inputs/test.patch
test ! -e /inputs/model.patch
if git -C /testbed cat-file -e {fix}^{{commit}} 2>/dev/null; then exit 1; fi
python --version
javac -version
sha256sum /usr/lib/x86_64-linux-gnu/libffi_pic.a
'''.format(base=base, fix=fix)
        process = subprocess.run(["docker", "run", "--rm", "--network", "none", image,
                                  "bash", "-lc", audit], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out / "image-audit.stdout.raw.log").write_bytes(process.stdout)
        (out / "image-audit.stderr.raw.log").write_bytes(process.stderr)
        if process.returncode:
            raise RuntimeError("Clean image audit failed")
        inspected = json.loads(subprocess.check_output(["docker", "image", "inspect", image]))[0]
        result.update(status="success", reason="standard_base_build_and_clean_image_audit_passed",
                      image={"name": image, "id": inspected["Id"], "repo_digests": inspected.get("RepoDigests", [])})
        write_json(out / "image-audit.json", dict(
            base_commit=base, working_tree_clean=True, fix_commit_present=False,
            model_patch_present=False, test_patch_present=False, gold_patch_present=False,
            evaluation_assets_injected_at_runtime=True, project_binaries_present=False,
            current_jni_compiled_during_each_evaluation=True, network_disabled_during_audit=True,
        ))
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        result["error"] = str(error)
    result["finished_at"] = utc_now()
    write_json(out / "summary.json", result)
    write_json(CASE / "verification/builds/latest.json", result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
