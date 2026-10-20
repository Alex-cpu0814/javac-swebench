"""Run 64-bit allocator-selection and pointer-width controls in separate JVMs."""
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
if repo != Path("/testbed") or out != Path("/results"):
    raise SystemExit("Unexpected evaluation paths")
test_root = repo / "config/tests/case074"
classes = repo / "bin/classes/benchmark"

builds = [
    ["gcc", "-std=c11", "-shared", "-fPIC", "-I/opt/java/openjdk/include",
     "-I/opt/java/openjdk/include/linux", "-o", str(out / "libpointerprobe.so"),
     str(test_root / "pointer_size.c")],
    ["gcc", "-std=c11", "-shared", "-fPIC", "-o", str(out / "libjemalloc.so"),
     str(test_root / "jemalloc_stub.c")],
    ["javac", "-source", "8", "-target", "8", "-encoding", "UTF-8",
     "-cp", str(classes), "-d", str(classes),
     str(test_root / "org/lwjgl/system/PointerInitializationProbe.java")],
]
with (out / "test-compilation.private.log").open("wb") as log:
    for command in builds:
        result = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            print(json.dumps({"phase": "test_compilation", "exit_code": result.returncode,
                              "infrastructure_error": True, "tests": {}}))
            raise SystemExit(2)

tests = {}
for mode in ("pointerWidth", "allocatorSelection"):
    command = [
        "java", "-Djava.library.path=" + str(out),
        "-XX:ErrorFile=" + str(out / "hs_err-%p.log"),
        "-cp", str(classes), "org.lwjgl.system.PointerInitializationProbe", mode,
    ]
    with (out / (mode + ".private.log")).open("wb") as log:
        try:
            result = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=60)
        except subprocess.TimeoutExpired:
            print(json.dumps({"phase": "runtime", "infrastructure_error": True,
                              "reason": "timeout", "tests": tests}))
            raise SystemExit(2)
    status = "passed" if result.returncode == 0 else "failed" if result.returncode == 1 else "error"
    tests["org.lwjgl.system.PointerInitializationProbe::" + mode] = {
        "status": status, "exit_code": result.returncode,
    }

report = {"oracle_type": "runtime_behavior", "phase": "runtime",
          "infrastructure_error": any(item["status"] == "error" for item in tests.values()),
          "tests": tests}
(out / "sanitized_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
raise SystemExit(2 if report["infrastructure_error"] else
                 0 if all(item["status"] == "passed" for item in tests.values()) else 1)
