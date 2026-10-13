"""Run candidate and existing regressions; expose only categorized outcomes."""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
classes = ["org.lwjgl.vulkan.DebugUtilsTest", "org.lwjgl.system.MemoryUtilTest", "org.lwjgl.system.StackTest", "org.lwjgl.system.BufferTest", "org.lwjgl.system.libffi.LibFFITest"]
fixture = repo / "bin/test-fixtures/libdebug_utils_fixture.so"
fixture.parent.mkdir(parents=True, exist_ok=True)
def run(command, phase):
    with (out / (phase + ".private.log")).open("w", encoding="utf-8") as log:
        try:
            result = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        except subprocess.TimeoutExpired:
            print(json.dumps({"phase": phase, "infrastructure_error": True, "category": "timeout"})); sys.exit(2)
    if phase != "testng" and result.returncode:
        print(json.dumps({"phase": phase, "infrastructure_error": True, "exit_code": result.returncode})); sys.exit(2)
    return result.returncode

run(["gcc", "-shared", "-fPIC", "-std=c99", "-Wall", "-Wextra", "-Werror", "-I" + str(repo / "modules/lwjgl/vulkan/src/main/c"), str(repo / "modules/lwjgl/vulkan/src/test/c/debug_utils_fixture.c"), "-o", str(fixture)], "fixture_compilation")
# Use current build products, never an installed LWJGL jar or native library.
classpath = ":".join(str(repo / p) for p in ["bin/classes/test", "bin/classes/lwjgl/core", "bin/classes/lwjgl/vulkan", "bin/libs/java/*"])
sources = [repo / "modules/lwjgl/vulkan/src/test/java/org/lwjgl/vulkan/DebugUtilsTest.java"] + [repo / ("modules/lwjgl/core/src/test/java/" + cls.replace(".", "/") + ".java") for cls in classes[1:]]
(repo / "bin/classes/test").mkdir(parents=True, exist_ok=True)
run(["javac", "-cp", classpath, "-d", str(repo / "bin/classes/test"), *map(str, sources)], "test_compilation")
native = repo / "bin/libs/native/linux/x64/org/lwjgl"
if not (native / "liblwjgl.so").is_file():
    print(json.dumps({"phase": "dynamic_loading", "infrastructure_error": True, "category": "missing_current_native_library"})); sys.exit(2)
code = run(["java", "-Dorg.lwjgl.librarypath=" + str(native), "-Dorg.lwjgl.vulkan.explicitInit=true", "-Dorg.lwjgl.vulkan.debugUtilsFixture=" + str(fixture), "-cp", classpath, "org.testng.TestNG", "-testclass", ",".join(classes), "-d", str(out / "testng"), "-verbose", "0"], "testng")
xml_path = out / "testng/testng-results.xml"
if not xml_path.exists():
    print(json.dumps({"phase": "collection", "infrastructure_error": True, "exit_code": code, "category": "missing_testng_results"})); sys.exit(2)
tree = ET.parse(xml_path)
nodes = {}
configurations = []
for cls in tree.findall(".//class"):
    for method in cls.findall("test-method"):
        item = {"status": method.attrib["status"], "exception_type": (method.find("exception").attrib.get("class") if method.find("exception") is not None else None)}
        if method.attrib.get("is-config") == "true":
            configurations.append(item)
        else:
            key = cls.attrib["name"] + "::" + method.attrib["name"]
            if key in nodes:
                # Data-provider invocations share an ID; preserve all outcomes.
                nodes[key].setdefault("invocations", []).append(item)
                if item["status"] != "PASS": nodes[key]["status"] = item["status"]
            else: nodes[key] = item
target_prefix = classes[0] + "::"
expected = {target_prefix + method for method in ["testNameInstance", "testNamePhysicalDevice", "testNameDevice"]}
infra = not expected.issubset(nodes) or any(c["status"] != "PASS" for c in configurations) or any(n["status"] == "SKIP" for n in nodes.values()) or code < 0 or code not in (0, 1)
report = {"phase": "call", "exit_code": code, "infrastructure_error": infra, "collected": expected.issubset(nodes), "nodes": nodes, "configuration_outcomes": configurations, "native_library": str(native / "liblwjgl.so"), "fixture": str(fixture), "skipped": any(n["status"] == "SKIP" for n in nodes.values()), "xfail": False}
(out / "sanitized_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"result_file": str(out / "sanitized_results.json"), "phase": report["phase"], "infrastructure_error": infra, "collected": report["collected"], "targets": {k: v for k, v in nodes.items() if k.startswith(target_prefix)}, "regression_nodes": len(nodes) - 3, "regression_failed": sum(v["status"] != "PASS" for k, v in nodes.items() if not k.startswith(target_prefix))}))
sys.exit(2 if infra else (0 if all(n["status"] == "PASS" for n in nodes.values()) else 1))
