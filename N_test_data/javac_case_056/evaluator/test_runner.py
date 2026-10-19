"""Execute protected F2P and the existing Vulkan test through TestNG XMLReporter."""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
classes = ["org.lwjgl.vulkan.VkFramebufferCreateInfoTest", "org.lwjgl.vulkan.VulkanTest"]
expected = {
    classes[0] + "::testNullAttachmentsPreserveAttachmentCount",
    classes[0] + "::testNullAttachmentsPassGeneratedValidation",
    classes[1] + "::testParse",
}


def execute(command, phase):
    with (out / (phase + ".private.log")).open("wb") as log:
        try:
            process = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        except subprocess.TimeoutExpired:
            print(json.dumps({"phase": phase, "category": "timeout", "infrastructure_error": True}))
            sys.exit(2)
    if phase != "testng" and process.returncode:
        print(json.dumps({"phase": phase, "exit_code": process.returncode, "infrastructure_error": True}))
        sys.exit(2)
    return process.returncode


cp = ":".join(str(repo / path) for path in [
    "bin/classes/test", "bin/classes/lwjgl/core", "bin/classes/lwjgl/vulkan", "bin/libs/java/*",
])
dest = repo / "bin/classes/test"
dest.mkdir(parents=True, exist_ok=True)
sources = [repo / ("modules/lwjgl/vulkan/src/test/java/" + name.replace(".", "/") + ".java") for name in classes]
execute(["javac", "-encoding", "UTF-8", "-cp", cp, "-d", str(dest), *map(str, sources)], "test_compilation")
native = repo / "bin/libs/native/linux/x64/org/lwjgl"
if not (native / "liblwjgl.so").is_file():
    print(json.dumps({"phase": "dynamic_loading", "infrastructure_error": True, "category": "missing_current_native_library"}))
    sys.exit(2)
code = execute([
    "java", "-Dorg.lwjgl.librarypath=" + str(native), "-Dorg.lwjgl.vulkan.explicitInit=true",
    "-cp", cp, "org.testng.TestNG", "-usedefaultlisteners", "false",
    "-listener", "org.testng.reporters.XMLReporter", "-testclass", ",".join(classes),
    "-d", str(out / "testng"), "-verbose", "0",
], "testng")
xml = out / "testng/testng-results.xml"
if not xml.is_file():
    print(json.dumps({"phase": "collection", "category": "missing_testng_results", "infrastructure_error": True}))
    sys.exit(2)
nodes, configurations = {}, []
for cls in ET.parse(xml).findall(".//class"):
    for method in cls.findall("test-method"):
        exception = method.find("exception")
        item = {"status": method.attrib["status"],
                "exception_type": exception.get("class") if exception is not None else None}
        if method.get("is-config") == "true":
            configurations.append(item)
        else:
            name = cls.attrib["name"] + "::" + method.attrib["name"]
            if name in nodes:
                raise RuntimeError("Duplicate test ID: " + name)
            nodes[name] = item
infra = set(nodes) != expected or code not in (0, 1) or any(
    item["status"] == "SKIP" for item in nodes.values()
) or any(item["status"] != "PASS" for item in configurations)
report = dict(phase="call", exit_code=code, infrastructure_error=infra, collected=expected.issubset(nodes),
              nodes=nodes, configuration_outcomes=configurations, native_library=str(native / "liblwjgl.so"),
              skipped=any(item["status"] == "SKIP" for item in nodes.values()), xfail=False)
(out / "sanitized_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))
sys.exit(2 if infra else (0 if all(item["status"] == "PASS" for item in nodes.values()) else 1))
