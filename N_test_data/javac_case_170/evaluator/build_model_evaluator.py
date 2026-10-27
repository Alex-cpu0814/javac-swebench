#!/usr/bin/env python3
"""Build and audit the isolated Base-only image, without solution or private tests."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--docker', default='docker')
parser.add_argument('--image')
parser.add_argument('--run-id', default='build-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
args = parser.parse_args()
if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-' for c in args.run_id):
    parser.error('unsafe run id')
config = json.loads((ROOT / 'evaluator/case_config.json').read_text())
image = args.image or config.get('build_image', config['image'])
out = ROOT / 'verification/builds' / args.run_id
out.mkdir(parents=True, exist_ok=False)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command, filename):
    with (out / filename).open('wb') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit('Failed ({}): {}'.format(result.returncode, out / filename))
run([sys.executable, str(ROOT / 'analysis/prepare_image_context.py')], 'prepare-context.raw.log')
context = ROOT / 'evaluator/image/context'
record = json.loads((ROOT / 'analysis/image_context.json').read_text())
assert {p.name: sha(p) for p in context.iterdir() if p.is_file()} == record['assets']
with tempfile.TemporaryDirectory(prefix='case170-image-') as temp:
    stage = Path(temp)
    (stage / 'context').mkdir()
    shutil.copyfile(ROOT / 'evaluator/image/Dockerfile', stage / 'Dockerfile')
    for name in record['assets']:
        shutil.copyfile(context / name, stage / 'context' / name)
    run([args.docker, 'build', '--progress=plain', '-t', image, str(stage)], 'docker-build.raw.log')
info = json.loads(subprocess.check_output([args.docker, 'image', 'inspect', image]))[0]
audit_code = '''import hashlib,json,pathlib,subprocess
r=pathlib.Path('/testbed')
c=json.loads(input())
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==c['base_commit']
assert not subprocess.check_output(['git','status','--porcelain']).strip()
assert subprocess.run(['git','cat-file','-e',c['fix_commit']],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
assert not (r/'benchmark-tests').exists() and not (r/'target').exists()
assert not pathlib.Path('/inputs').exists() and not pathlib.Path('/benchmark').exists()
actual={p.relative_to(r).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and '.git' not in p.relative_to(r).parts}
assert actual==c['files']
print('BASE_ONLY_IMAGE_AUDIT_OK')
subprocess.run(['java','-version'],check=True)
subprocess.run(['python3','--version'],check=True)
subprocess.run(['ldd','--version'],check=True)
'''
provenance = json.loads((ROOT / 'analysis/source_provenance.json').read_text())
audit_input = {'base_commit': config['base_commit'], 'fix_commit': config['fix_commit'],
               'files': provenance['sources']['base']['files']}
audit = subprocess.run([args.docker, 'run', '--rm', '-i', '--network', 'none', '--cap-drop', 'ALL',
                       '--security-opt', 'no-new-privileges', info['Id'], 'python3', '-c', audit_code],
                       input=json.dumps(audit_input).encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(out / 'image-audit.raw.log').write_bytes(audit.stdout)
assert audit.returncode == 0, 'Base-only audit failed: ' + str(out)
summary = {'status': 'built_and_audited', 'image': image, 'image_id': info['Id'],
           'base_commit': config['base_commit'], 'fix_object_absent': True,
           'private_tests_absent': True, 'compiled_project_absent': True,
           'context_sha256': record['assets'], 'dockerfile_sha256': sha(ROOT / 'evaluator/image/Dockerfile'),
           'builder_sha256': sha(Path(__file__)), 'audit_log_sha256': sha(out / 'image-audit.raw.log')}
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
