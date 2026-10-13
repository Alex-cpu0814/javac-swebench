"""Download the exact dependency URL specified by the Base Ant build."""
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

url = "https://build.lwjgl.org/release/3.3.1/linux/x64/core/libffi.a"
dest = Path("/testbed/bin/libs/native/linux/x64/org/lwjgl/libffi.a")
dest.parent.mkdir(parents=True, exist_ok=True)
if "--ubuntu-pic" in sys.argv:
    archive = Path("/usr/lib/x86_64-linux-gnu/libffi_pic.a")
    data = archive.read_bytes()
    package = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", "libffi-dev"], text=True)
    source = {"type": "ubuntu_pic_dependency", "package": "libffi-dev", "version": package, "archive": str(archive), "upstream_download_unavailable": True}
else:
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    source = {"type": "standard_upstream_dependency", "url": url}
assert data.startswith(b"!<arch>\n"), "Not a static archive"
dest.write_bytes(data)
record = {"requested_upstream_url": url, "source": source, "path": str(dest), "size": len(data), "sha256": hashlib.sha256(data).hexdigest(), "reason": "Provide a declared custom static dependency through Ant's supported offline mode; project JNI remains built from current sources. Ubuntu PIC mode is a dependency adaptation and is not the official upstream archive."}
Path("/workspace/native_dependency.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record))
