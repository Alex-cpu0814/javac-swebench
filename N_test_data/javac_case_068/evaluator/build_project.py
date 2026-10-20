"""Compile the candidate's generated OpenVR Java binding from the Base checkout."""
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1] if len(sys.argv) > 1 else "/testbed").resolve()
if repo != Path("/testbed") or not (repo / "build.xml").is_file():
    raise SystemExit("Expected isolated /testbed LWJGL checkout")

source = repo / "modules/lwjgl/openvr/src/generated/java/org/lwjgl/openvr/VRCompositor.java"
classes = repo / "bin/classes/benchmark"
classes.mkdir(parents=True, exist_ok=True)
command = [
    "javac", "-source", "8", "-target", "8", "-encoding", "UTF-8",
    "-cp", "/opt/benchmark/lib/*", "-d", str(classes), str(source),
]
print(json.dumps({"phase": "source_build", "command": command}), flush=True)
raise SystemExit(subprocess.run(command, cwd=repo).returncode)
