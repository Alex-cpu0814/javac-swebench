"""Cold standard Ant build: regenerate bindings and compile current Java/JNI sources."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default="/testbed")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if repo != Path("/testbed") or not (repo / "build.xml").is_file():
        raise SystemExit("Expected the isolated /testbed checkout")
    names = sorted({
        item.attrib.get("name", item.attrib.get("property", ""))
        for item in ET.parse(repo / "config/build-bindings.xml").iter()
        if item.attrib.get("name", item.attrib.get("property", "")).startswith("binding.")
    } - {"binding.DISABLE_CHECKS"})
    flags = ["-D" + name + "=" + ("true" if name == "binding.vulkan" else "false") for name in names]
    # Remove dynamic outputs so no Base binary or Maven native library can mask candidate changes.
    for library in (repo / "bin/libs/native").rglob("*.so"):
        library.unlink()
    command = ["ant", "-Dbuild.type=release/3.3.0",
               "-Dbuild.offline=" + ("true" if args.offline else "false"),
               *flags, "clean-kotlin", "clean-java", "clean-native", "compile-templates", "compile-native"]
    print(json.dumps({"phase": "standard_ant_build", "enabled_modules": ["core", "vulkan"],
                      "cold_rebuild": True, "command": command}), flush=True)
    result = subprocess.run(command, cwd=repo)
    if result.returncode:
        return result.returncode
    native = repo / "bin/libs/native/linux/x64/org/lwjgl/liblwjgl.so"
    if not native.is_file():
        raise SystemExit("Current JNI library was not built")
    print(json.dumps({"current_native_library": str(native),
                      "sha256": hashlib.sha256(native.read_bytes()).hexdigest()}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
