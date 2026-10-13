"""Use the pinned repository's standard Ant build, core + Vulkan only."""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo = Path(sys.argv[1] if len(sys.argv) > 1 else "/testbed")
names = sorted({e.attrib.get("name", e.attrib.get("property", "")) for e in ET.parse(repo / "config/build-bindings.xml").iter() if e.attrib.get("name", e.attrib.get("property", "")).startswith("binding.")} - {"binding.DISABLE_CHECKS"})
flags = ["-D" + name + "=" + ("true" if name == "binding.vulkan" else "false") for name in names]
command = ["ant", "-Dbuild.type=release/3.3.1", "-Dbuild.offline=" + ("true" if "--offline" in sys.argv else "false"), *flags, "compile-templates", "compile-native"]
print(json.dumps({"phase": "standard_ant_build", "enabled_modules": ["core", "vulkan"], "command": command}), flush=True)
sys.exit(subprocess.run(command, cwd=repo).returncode)
