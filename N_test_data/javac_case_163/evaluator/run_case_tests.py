"""Run real child-JVM controls and unchanged upstream JUnit tests (Python 3.5+)."""
from __future__ import print_function
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

RESULTS = Path('/results')
OUT = Path('/testbed/target/case163')
MANIFEST = json.loads(Path('/benchmark/upstream_tests.json').read_text(encoding='utf-8'))
CLASSPATH = str(OUT / 'classes') + ':' + str(OUT / 'testclasses')
JAVA = '/opt/java/jdk8u292-b10/bin/java'
JVM = [JAVA, '-Xint', '-Xms16m', '-Xmx64m', '-XX:+UseSerialGC', '-XX:ActiveProcessorCount=2']


def execute(command, prefix, timeout):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        stdout, stderr = process.communicate()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    Path(str(prefix) + '.stdout.log').write_bytes(stdout)
    Path(str(prefix) + '.stderr.log').write_bytes(stderr)
    record = {'command': command, 'exit_code': process.returncode, 'timed_out': timed_out,
              'stdout_sha256': hashlib.sha256(stdout).hexdigest(),
              'stderr_sha256': hashlib.sha256(stderr).hexdigest()}
    Path(str(prefix) + '.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return record, stdout.decode('utf-8', 'replace')


def emit(test_id, status):
    owner, method = test_id.rsplit('.', 1)
    print('{} ({}) ... {}'.format(method, owner, status), flush=True)


failed = False
for old in (False, True):
    command = list(JVM) + ['-cp', CLASSPATH, 'org.newsclub.net.unix.Issue81GlibcProbe']
    name = 'old-glibc' if old else 'modern-glibc'
    if old:
        command = ['/opt/tools/qemu-x86_64-static', '-L', '/opt/legacy'] + command
    result, stdout = execute(command, RESULTS / 'children' / name, 30)
    lines = stdout.splitlines()
    passed = result['exit_code'] == 0 and not result['timed_out']
    passed = passed and lines.count('ISSUE81_PROBE_OK') == 1
    for iteration in range(3):
        passed = passed and all(lines.count(prefix + str(iteration)) == 1
                               for prefix in ('BEFORE_BIND=', 'AFTER_BIND=', 'ROUNDTRIP_OK='))
    method = 'testAutomaticFallbackOldGlibc' if old else 'testModernGlibcRoundTrip'
    emit('org.newsclub.net.unix.Issue81CompatibilityTest.' + method, 'ok' if passed else 'FAIL')
    failed = failed or not passed

reports = RESULTS / 'upstream'
reports.mkdir(exist_ok=True)
command = [JAVA, '-cp', CLASSPATH + ':/opt/deps/junit-console.jar:/opt/deps/annotations.jar',
           'org.junit.platform.console.ConsoleLauncher', '--disable-ansi-colors',
           '--reports-dir', str(reports), '--details', 'summary', '--fail-if-no-tests']
for test_id in MANIFEST['test_ids']:
    owner, method = test_id.rsplit('.', 1)
    command += ['--select-method', owner + '#' + method]
result, unused_stdout = execute(command, RESULTS / 'upstream-run', 180)
observed = {}
parse_error = None
try:
    for report in reports.glob('*.xml'):
        for test in ET.parse(str(report)).getroot().iter('testcase'):
            method = test.get('name', '')
            if not method.endswith('()'):
                raise ValueError('Unexpected JUnit testcase name: ' + method)
            test_id = test.get('classname', '') + '.' + method[:-2]
            if test_id in observed:
                raise ValueError('Duplicate JUnit testcase: ' + test_id)
            if test.find('failure') is not None or test.find('error') is not None:
                status = 'FAIL'
            elif test.find('skipped') is not None:
                status = 'skipped'
            else:
                status = 'ok'
            observed[test_id] = status
    if set(observed) != set(MANIFEST['test_ids']):
        raise ValueError('JUnit testcase set differs from protected manifest')
except Exception as error:
    parse_error = str(error)
if parse_error:
    print('UPSTREAM_REPORT_ERROR=' + parse_error, flush=True)
for test_id in MANIFEST['test_ids']:
    status = observed.get(test_id, 'ERROR') if parse_error is None else 'ERROR'
    emit(test_id, status)
    failed = failed or status != 'ok'
if result['exit_code'] != 0 or result['timed_out'] or parse_error:
    failed = True
sys.exit(1 if failed else 0)
