"""Restore Unix line endings in the pinned LWJGL-CI Git mirror snapshot."""
from pathlib import Path

root = Path("/opt/dyncall")
changed = []
for path in root.rglob("*"):
    if not path.is_file():
        continue
    data = path.read_bytes()
    if b"\x00" in data or b"\r\n" not in data:
        continue
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        continue
    path.write_bytes(data.replace(b"\r\n", b"\n"))
    changed.append(str(path.relative_to(root)))
print("Normalized CRLF in", len(changed), "dyncall text files")
