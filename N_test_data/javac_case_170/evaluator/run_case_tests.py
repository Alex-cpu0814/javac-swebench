"""Run fresh-JVM noexec integration cases and unchanged, frozen upstream JUnit cases."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path('/testbed')
OUT = ROOT / 'target/case170'
RESULT = Path('/results')
MANIFEST = json.loads(Path('/benchmark/upstream_tests.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--discover', action='store_true')
args = parser.parse_args()
RESULT.mkdir(parents=True, exist_ok=True)
deps = ':'.join(str(p) for p in sorted(Path('/opt/deps').glob('*.jar')))
cp = str(OUT / 'classes') + ':' + str(OUT / 'testclasses') + ':' + deps
java = ['java', '-Xmx128m', '-XX:+UseSerialGC', '-XX:ActiveProcessorCount=2']
statuses = {}

def invoke(argv, name, cwd=ROOT, timeout=90):
    try:
        result = subprocess.run([str(x) for x in argv], cwd=str(cwd), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout)
        text = result.stdout.decode('utf-8', errors='replace')
        code = result.returncode
    except subprocess.TimeoutExpired as error:
        text = (error.stdout or b'').decode('utf-8', errors='replace') + '\nBENCHMARK_TIMEOUT\n'
        code = None
    (RESULT / (name + '.raw.log')).write_text(text, encoding='utf-8')
    (RESULT / (name + '.json')).write_text(json.dumps({'command': [str(x) for x in argv],
              'cwd': str(cwd), 'exit_code': code, 'timeout': code is None}, indent=2) + '\n')
    return code, text

if not args.discover:
    for name, flags, positive, expected in (
            ('exec_loading', (False, False, False), True, 0),
            ('noexec_home_fallback', (True, False, False), True, 1),
            ('noexec_cwd_fallback', (True, True, False), True, 2),
            ('all_noexec_rejected', (True, True, True), False, None)):
        paths = []
        for index, blocked in enumerate(flags):
            path = Path('/case-noexec' if blocked else '/case-exec') / (name + str(index))
            path.mkdir()
            paths.append(path)
        command = java + ['-Djava.io.tmpdir=' + str(paths[0]),
                         '-Dorg.newsclub.net.unix.library.tmpdir=' + str(paths[0]),
                         '-Duser.home=' + str(paths[1]), '-Duser.dir=' + str(paths[2]),
                         '-cp', cp, 'org.newsclub.net.unix.NoexecProbe']
        code, text = invoke(command, name, cwd=paths[2], timeout=30)
        try:
            assert code is not None, 'child JVM timeout'
            assert 'LOADER_ORIGIN=file:/testbed/target/case170/classes/' in text, 'candidate class origin missing'
            for path in paths:
                assert 'WRITABLE=' + str(path) + '\n' in text, 'write/read control failed'
            mounts = dict(line[6:].split(' ', 1) for line in text.splitlines() if line.startswith('MOUNT='))
            assert 'noexec' in mounts['/case-noexec'].split(','), 'real noexec mount missing'
            assert 'noexec' not in mounts['/case-exec'].split(','), 'exec mount unexpectedly blocked'
            if positive:
                assert code == 0, 'native initialization failed (see child raw log)'
                assert text.count('NOEXEC_PROBE_OK\n') == 1, 'success marker missing'
                for i in range(3):
                    assert text.count('ROUNDTRIP_OK=' + str(i) + '\n') == 1, 'native roundtrip missing'
                mappings = [line[15:] for line in text.splitlines() if line.startswith('NATIVE_MAPPING=')]
                assert mappings and all(line.startswith(str(paths[expected]) + '/') for line in mappings), 'incorrect library extraction/mapping path'
            else:
                assert code == 1 and 'NOEXEC_PROBE_OK' not in text, 'all-blocked path falsely succeeded'
                failures = [line for line in text.splitlines() if 'UnsatisfiedLinkError' in line and 'failed to map segment from shared object' in line]
                assert failures, 'missing real noexec System.load failure'
                assert all('perm' not in line.lower() for line in failures), 'wrong error-message trigger'
            statuses['benchmark.noexec.' + name] = 'PASSED'
        except (AssertionError, KeyError) as error:
            statuses['benchmark.noexec.' + name] = 'FAILED'
            (RESULT / (name + '.assertion.log')).write_text(str(error) + '\n')

reports = RESULT / 'junit'
command = java + ['-jar', '/opt/deps/junit-platform-console-standalone-1.10.0.jar', 'execute',
                  '--disable-ansi-colors', '--details=summary', '--class-path', cp,
                  '--reports-dir', str(reports)]
for name in MANIFEST['selected_classes']:
    command += ['--select-class', name]
code, text = invoke(command, 'upstream-junit', timeout=240)
observed = {}
duplicates = []
for path in sorted(reports.glob('TEST-junit-jupiter.xml')):
    for node in ET.parse(str(path)).getroot().iter('testcase'):
        test_id = node.attrib['classname'] + '.' + node.attrib['name']
        if test_id in observed:
            duplicates.append(test_id)
        status = 'SKIPPED' if node.find('skipped') is not None else (
                 'FAILED' if node.find('failure') is not None or node.find('error') is not None else 'PASSED')
        observed[test_id] = status
(RESULT / 'upstream_observed.json').write_text(json.dumps(observed, indent=2) + '\n')
if args.discover:
    print(json.dumps({'exit_code': code, 'observed': observed, 'duplicates': duplicates}, indent=2))
    sys.exit(0 if code == 0 and observed and not duplicates else 1)
expected = set(MANIFEST['test_ids'])
valid = (code == 0 or code == 1) and not duplicates and set(observed) == expected and bool(expected)
for test_id in sorted(expected):
    statuses[test_id] = observed.get(test_id, 'MISSING') if valid else 'FAILED'
if not valid:
    (RESULT / 'upstream_structure_error.json').write_text(json.dumps({'expected': sorted(expected),
                'observed': sorted(observed), 'duplicates': duplicates, 'exit_code': code}, indent=2))
for test_id, status in sorted(statuses.items()):
    cls, method = test_id.rsplit('.', 1)
    print('{} ({}) ... {}'.format(method, cls, 'ok' if status == 'PASSED' else 'FAIL'), flush=True)
sys.exit(0 if valid and all(value == 'PASSED' for value in statuses.values()) else 1)
