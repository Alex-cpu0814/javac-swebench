"""Build and audit a clean LWJGL Base image for case 074."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile


CASE = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image")
    parser.add_argument("--source-repo", type=Path)
    parser.add_argument("--repo-url", default="https://github.com/LWJGL/lwjgl3.git")
    parser.add_argument("--build-id", default="case-074-build-local")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    if not args.build_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in args.build_id):
        raise SystemExit("Invalid build ID")
    config = json.loads((CASE / "evaluator/case_config.json").read_text(encoding="utf-8"))
    image = args.image or config["build_image"]
    out = CASE / "verification/builds" / args.build_id
    out.mkdir(parents=True, exist_ok=False)
    base = config["base_commit"]
    fix = config["fix_commit"]
    result = {"build_id": args.build_id, "image": image, "base_commit": base, "status": "error"}
    default_source = CASE.parents[2] / "_work/lwjgl3-100"
    source = args.source_repo or (default_source if (default_source / ".git").exists() else None)
    source_url = str(source.resolve()) if source else args.repo_url
    try:
        with tempfile.TemporaryDirectory(prefix="case074-build-") as temporary:
            context = Path(temporary)
            bare = context / "base.git"
            with (out / "source-preparation.raw.log").open("wb") as log:
                subprocess.run(["git", "init", "--bare", str(bare)], check=True, stdout=log, stderr=log)
                subprocess.run([
                    "git", "-c", "protocol.file.allow=always", "--git-dir", str(bare),
                    "fetch", "--no-tags", "--depth=1", source_url, base,
                ], check=True, stdout=log, stderr=log, timeout=300)
            bare.joinpath("HEAD").write_text(base + "\n", encoding="ascii")
            bare.joinpath("config").write_text(
                "[core]\nrepositoryformatversion = 0\nfilemode = true\nbare = false\n", encoding="ascii")
            present = subprocess.run(
                ["git", "--git-dir", str(bare), "cat-file", "-e", fix + "^{commit}"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if present.returncode == 0:
                raise RuntimeError("Fix commit leaked into Base image context")
            with tarfile.open(context / "base-git.tar.gz", "w:gz") as archive:
                for name in ("HEAD", "config", "shallow", "objects"):
                    if bare.joinpath(name).exists():
                        archive.add(bare / name, arcname=name)
                (bare / "refs").mkdir(exist_ok=True)
                archive.add(bare / "refs", arcname="refs")
            shutil.copyfile(CASE / "evaluator/image/Dockerfile", context / "Dockerfile")
            (context / ".dockerignore").write_text(
                "*\n!Dockerfile\n!base-git.tar.gz\n", encoding="utf-8")
            command = ["docker", "build", "--platform", "linux/amd64", "--progress=plain",
                       "-t", image, "--build-arg", "BASE_COMMIT=" + base,
                       "--build-arg", "INSTANCE_ID=" + config["instance_id"], str(context)]
            with (out / "docker-build.stdout.raw.log").open("wb") as stdout, \
                    (out / "docker-build.stderr.raw.log").open("wb") as stderr:
                subprocess.run(command, check=True, stdout=stdout, stderr=stderr, timeout=args.timeout)

        audit = "\n".join([
            "set -euo pipefail",
            'test "$(git -C /testbed rev-parse HEAD)" = "' + base + '"',
            'test -z "$(git -C /testbed status --porcelain)"',
            "test ! -e /testbed/bin/classes/benchmark",
            "test ! -e /testbed/config/tests/case074/org/lwjgl/system/PointerInitializationProbe.java",
            "test ! -e /testbed/config/tests/case074/pointer_size.c",
            "test ! -e /benchmark/run_evaluation.sh",
            "test ! -e /inputs/model.patch",
            "test ! -e /inputs/test.patch",
            "if git -C /testbed cat-file -e " + fix + "^{commit} 2>/dev/null; then exit 1; fi",
            "test ! -e /testbed/config/tests/case074",
            "java -version",
            "python3 --version",
        ])
        process = subprocess.run(
            ["docker", "run", "--rm", "--network", "none", image, "bash", "-lc", audit],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        (out / "image-audit.stdout.raw.log").write_bytes(process.stdout)
        (out / "image-audit.stderr.raw.log").write_bytes(process.stderr)
        if process.returncode:
            raise RuntimeError("Clean Base image audit failed")
        inspected = json.loads(subprocess.check_output(["docker", "image", "inspect", image]))[0]
        result.update(status="success", image_id=inspected["Id"],
                      clean_base_verified=True, fix_object_absent=True,
                      protected_tests_absent=True, project_binaries_absent=True)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        result["error"] = str(error)
    write_json(out / "summary.json", result)
    write_json(CASE / "verification/builds/latest.json", result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
