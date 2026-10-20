"""Download and verify the pinned 2019 Kotlin/Maven build inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

CASE = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, path: Path, expected: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and digest(path) == expected:
        print("verified", path)
        return
    temporary = path.with_name(path.name + ".download")
    with urllib.request.urlopen(url, timeout=180) as response, temporary.open("wb") as output:
        while block := response.read(1024 * 1024):
            output.write(block)
    if digest(temporary) != expected:
        temporary.unlink()
        raise RuntimeError("SHA-256 mismatch: " + url)
    temporary.replace(path)
    print("downloaded and verified", path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-root", type=Path, default=CASE.parents[2] / "_work/lwjgl3-2019-deps")
    args = parser.parse_args()
    root = args.cache_root.resolve()
    manifest = json.loads((CASE / "evaluator/dependency-cache/manifest.json").read_text(encoding="utf-8"))
    kotlin = manifest["kotlin"]
    archive = root / "kotlin-compiler-1.3.50.zip"
    fetch(kotlin["url"], archive, kotlin["sha256"])
    compiler = root / "bin/libs/kotlinc"
    if not (compiler / "build.txt").is_file() or (compiler / "build.txt").read_text(encoding="utf-8").strip() != kotlin["build"]:
        with zipfile.ZipFile(archive) as z:
            if any(not name.startswith("kotlinc/") or ".." in Path(name).parts for name in z.namelist()):
                raise RuntimeError("Unexpected Kotlin archive path")
            z.extractall(root / "bin/libs")
    if (compiler / "build.txt").read_text(encoding="utf-8").strip() != kotlin["build"]:
        raise RuntimeError("Kotlin build marker mismatch")
    for artifact in manifest["java_jars"]:
        fetch(artifact["url"], root / "bin/libs/java" / artifact["name"], artifact["sha256"])
    print("Pinned dependency cache ready:", root / "bin/libs")


if __name__ == "__main__":
    main()
