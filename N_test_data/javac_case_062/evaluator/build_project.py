"""Cold Ant build of current LWJGL Core/LLVM Java and JNI bindings."""
import json
import subprocess
import sys
from pathlib import Path

repo=Path(sys.argv[1] if len(sys.argv)>1 else '/testbed').resolve()
if repo != Path('/testbed') or not (repo/'build.xml').is_file():
    raise SystemExit('Expected isolated /testbed checkout')
flags=['-Dbuild.type=release/3.2.2','-Dbuild.offline=true','-Dbinding.llvm=true']
import xml.etree.ElementTree as ET
names={e.attrib.get('name',e.attrib.get('property','')) for e in ET.parse(repo/'config/build-bindings.xml').iter()}
flags.extend('-D'+name+'=false' for name in sorted(names) if name.startswith('binding.') and name not in ('binding.llvm','binding.DISABLE_CHECKS'))
cmd=['ant',*flags,'clean-kotlin','clean-java','clean-native','compile-templates','compile-native']
print(json.dumps({'phase':'source_build','command':cmd}),flush=True)
result=subprocess.run(cmd,cwd=repo)
if result.returncode:
    sys.exit(result.returncode)
for path in ('bin/libs/native/linux/x64/org/lwjgl/liblwjgl.so','bin/libs/native/linux/x64/org/lwjgl/llvm/liblwjgl_llvm.so'):
    if not (repo/path).is_file():
        raise SystemExit('Missing current native library: '+path)
