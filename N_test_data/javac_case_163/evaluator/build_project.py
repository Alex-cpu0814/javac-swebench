"""Source build adapter for the historical core JNI modules (Python 3.5+)."""
from __future__ import print_function
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path('/testbed')
OUT = ROOT / 'target/case163'
NS = {'m': 'http://maven.apache.org/POM/4.0.0'}
MANIFEST = json.loads(Path('/benchmark/upstream_tests.json').read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard():
    for name, expected in MANIFEST['source_sha256'].items():
        path = ROOT / name
        if not path.is_file() or digest(path) != expected:
            raise SystemExit('protected_upstream_test_modified: ' + name)


def run(argv):
    print('BUILD_ARGV=' + json.dumps([str(x) for x in argv]), flush=True)
    subprocess.check_call([str(x) for x in argv], cwd=str(ROOT))


guard()
OUT.mkdir(parents=True, exist_ok=True)
classes = OUT / 'classes'
tests = OUT / 'testclasses'
native = OUT / 'native'
for directory in (classes, tests, native):
    directory.mkdir(parents=True, exist_ok=True)
properties = {}
for pom in (ROOT / 'pom.xml', ROOT / 'junixsocket-native/pom.xml'):
    tree = ET.parse(str(pom)).getroot()
    for node in tree.findall('m:properties/*', NS):
        properties[node.tag.split('}', 1)[-1]] = node.text or ''
properties.update({'project.basedir': str(ROOT / 'junixsocket-native'),
                   'junixsocket.native.llvm.target': 'current'})


def expand(value):
    for unused in range(30):
        replacement = re.sub(r'\$\{([^}]+)\}', lambda m: properties.get(m.group(1), m.group(0)), value)
        if replacement == value:
            break
        value = replacement
    if '${' in value:
        raise ValueError('Unresolved native compiler property: ' + value)
    return value


options = None
for line in (ROOT / 'junixsocket-native/src/main/nar/aol.properties').read_text(encoding='utf-8').splitlines():
    if line.startswith('amd64.Linux.clang.c.options='):
        options = line.split('=', 1)[1]
        break
if options is None:
    raise SystemExit('Missing upstream amd64 Linux compiler options')
configured = shlex.split(expand(options))
flags = ['-fPIC']
index = 0
while index < len(configured):
    item = configured[index]
    if item == '-target':
        if configured[index + 1] != 'current':
            raise SystemExit('This evaluator targets the native Linux architecture')
        index += 2
        continue
    if item not in ('-finline-functions', '-Xcrossclang-with-and-without-lc'):
        flags.append(item)
    index += 1
print('NATIVE_FLAGS=' + json.dumps(flags), flush=True)
objects = {False: [], True: []}
for source in sorted((ROOT / 'junixsocket-native/src/main/c').rglob('*.c')):
    for nodeps in (False, True):
        suffix = '.nodeps.o' if nodeps else '.o'
        object_file = native / (source.stem + suffix)
        extra = ['-D__CROSSCLANG_NODEPS__=1'] if nodeps else []
        run(['clang'] + flags + extra + ['-c', source, '-o', object_file])
        objects[nodeps].append(object_file)
for nodeps in (False, True):
    suffix = '.nodeps.so' if nodeps else '.so'
    library = native / ('libjunixsocket-native-2.3.2' + suffix)
    run(['clang', '-shared'] + (['-nostdlib'] if nodeps else []) + objects[nodeps] + ['-o', library])

sources = []
for module in ('junixsocket-common', 'junixsocket-native-common'):
    sources += sorted(p for p in (ROOT / module / 'src/main/java').rglob('*.java') if p.name != 'module-info.java')
run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-d', classes] + sources)
resources = classes / 'lib/amd64-Linux-clang/jni'
resources.mkdir(parents=True, exist_ok=True)
for library in native.glob('*.so'):
    shutil.copyfile(str(library), str(resources / library.name))
for artifact in ('junixsocket-common', 'junixsocket-native-common'):
    metadata = classes / ('META-INF/maven/com.kohlschutter.junixsocket/' + artifact)
    metadata.mkdir(parents=True, exist_ok=True)
    (metadata / 'pom.properties').write_text('version=2.3.2\n', encoding='utf-8')
classpath = str(classes) + ':/opt/deps/junit-console.jar:/opt/deps/annotations.jar'
sources = sorted((ROOT / 'junixsocket-common/src/test/java').rglob('*.java'))
run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', classpath,
     '-d', tests] + sources)
guard()
artifacts = {p.relative_to(OUT).as_posix(): digest(p) for p in OUT.rglob('*') if p.is_file()}
Path('/results/build-artifacts.json').write_text(json.dumps(artifacts, indent=2) + '\n', encoding='utf-8')
