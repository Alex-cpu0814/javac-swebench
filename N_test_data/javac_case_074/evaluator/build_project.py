"""Compile the candidate's exact-commit Pointer.java against protected stubs."""
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1] if len(sys.argv) > 1 else "/testbed").resolve()
if repo != Path("/testbed") or not (repo / "build.xml").is_file():
    raise SystemExit("Expected isolated /testbed LWJGL checkout")

source = repo / "modules/core/src/main/java/org/lwjgl/system/Pointer.java"
test_root = repo / "config/tests/case074"
classes = repo / "bin/classes/benchmark"
classes.mkdir(parents=True, exist_ok=True)
command = [
    "javac", "-source", "8", "-target", "8", "-encoding", "UTF-8",
    "-d", str(classes),
    str(test_root / "org/lwjgl/PointerBuffer.java"),
    str(test_root / "org/lwjgl/system/MemoryAccess.java"),
    str(test_root / "org/lwjgl/system/MemoryUtil.java"),
    str(test_root / "org/lwjgl/system/AllocatorProbe.java"),
    str(source),
]
print(json.dumps({"phase": "source_build", "command": command}), flush=True)
raise SystemExit(subprocess.run(command, cwd=repo).returncode)
