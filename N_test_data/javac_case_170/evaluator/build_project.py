"""Compile the candidate core Java 8 sources against a pinned released JNI fixture."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path('/testbed')
OUT = ROOT / 'target/case170'
MANIFEST = json.loads(Path('/benchmark/upstream_tests.json').read_text())
for name, expected in MANIFEST['source_sha256'].items():
    p = ROOT / name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        raise SystemExit('protected_upstream_test_modified: ' + name)

def run(args):
    print('BUILD_ARGV=' + json.dumps([str(x) for x in args]), flush=True)
    subprocess.run([str(x) for x in args], cwd=str(ROOT), check=True)

classes = OUT / 'classes'
tests = OUT / 'testclasses'
classes.mkdir(parents=True, exist_ok=True)
tests.mkdir(parents=True, exist_ok=True)
source_root = ROOT / 'junixsocket-common/src'
sources = {}
# Upstream javaN folders contain compatibility replacements for JDK <= N.
# Apply the Java 15 stub before the Java 8 replacements, as the multi-release build does.
for layer in ('java', 'java15', 'java8', 'java7'):
    folder = source_root / 'main' / layer
    for p in sorted(folder.rglob('*.java')):
        if p.name != 'module-info.java':
            sources[p.relative_to(folder).as_posix()] = p
template = source_root / 'main/java-unresolved-properties/org/newsclub/net/unix/BuildProperties.java'
generated = OUT / 'generated/org/newsclub/net/unix/BuildProperties.java'
generated.parent.mkdir(parents=True, exist_ok=True)
text = template.read_text(encoding='utf-8')
version = re.search(r'<version>([^<]+)</version>', (ROOT / 'pom.xml').read_text(encoding='utf-8')).group(1)
values = {'project.version': version, 'git.build.version': version,
          'git.commit.id.abbrev': '71a134b', 'git.commit.id.full':
          '71a134bce58a22fb17a7a14f00799196c0c71a60', 'git.commit.time': '2023-09-29', 'git.dirty': 'true'}
for name, value in values.items():
    text = text.replace('${' + name + '}', value)
generated.write_text(text, encoding='utf-8')
sources['org/newsclub/net/unix/BuildProperties.java'] = generated
deps = ':'.join(str(p) for p in sorted(Path('/opt/deps').glob('*.jar')))
run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', deps,
     '-d', classes] + list(sources.values()))
resources = source_root / 'main/resources'
if resources.exists():
    shutil.copytree(resources, classes, dirs_exist_ok=True)
test_sources = {}
for layer in ('java', 'java15', 'java8'):
    folder = source_root / 'test' / layer
    for p in sorted(folder.rglob('*.java')):
        if p.name != 'module-info.java':
            test_sources[p.relative_to(folder).as_posix()] = p
test_sources['org/newsclub/net/unix/NoexecProbe.java'] = ROOT / 'benchmark-tests/org/newsclub/net/unix/NoexecProbe.java'
run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', str(classes) + ':' + deps,
     '-d', tests] + list(test_sources.values()))
print('BUILD_COMPLETE core_java_sources={} test_java_sources={} native_fixture=2.8.0'.format(
      len(sources), len(test_sources)), flush=True)
