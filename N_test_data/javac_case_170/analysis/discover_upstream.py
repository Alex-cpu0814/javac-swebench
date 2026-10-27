"""Run the scoped original JUnit classes on untouched Base before freezing IDs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--docker', default='docker')
parser.add_argument('--run-id', default='base-junit-discovery-v1')
parser.add_argument('--freeze', action='store_true')
args = parser.parse_args()
assert args.run_id and all(c.isalnum() or c in '-_.' for c in args.run_id)
config = json.loads((ROOT / 'evaluator/case_config.json').read_text())
image = json.loads(subprocess.check_output([args.docker, 'image', 'inspect', config['image']]))[0]['Id']
out = ROOT / 'verification/discovery' / args.run_id
out.mkdir(parents=True, exist_ok=False)
cmd = [args.docker, 'run', '--rm', '--network', 'none', '--cap-drop', 'ALL',
       '--security-opt', 'no-new-privileges',
       '--mount', 'type=bind,source={},target=/benchmark,readonly'.format(ROOT / 'evaluator'),
       '--mount', 'type=bind,source={},target=/inputs,readonly'.format(ROOT / 'patches'),
       '--mount', 'type=bind,source={},target=/results'.format(out),
       image, 'bash', '-c', 'git apply /inputs/test_patch.diff && python3 /benchmark/build_project.py > /results/build.raw.log 2>&1 && python3 /benchmark/run_case_tests.py --discover > /results/discovery.json']
result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=420)
(out / 'docker.raw.log').write_bytes(result.stdout)
record = {'image_id': image, 'exit_code': result.returncode, 'command': cmd,
          'assets_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in
             ('patches/test_patch.diff', 'evaluator/build_project.py', 'evaluator/run_case_tests.py', 'evaluator/upstream_tests.json')}}
(out / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
assert result.returncode == 0, 'Discovery failed: inspect ' + str(out)
data = json.loads((out / 'discovery.json').read_text())
assert not data['duplicates'] and data['observed'] and all(x == 'PASSED' for x in data['observed'].values())
if args.freeze:
    manifest_path = ROOT / 'evaluator/upstream_tests.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['test_ids'] = sorted(data['observed'])
    manifest['selection_reason'] = 'Scoped loader-adjacent coverage: address serialization/URI and large native ports, socket initialization/metadata, real byte I/O, socket factories. Not the full upstream suite.'
    manifest['excluded_ids'] = []
    manifest['exclusion_reason'] = 'None among the selected classes; all discovered cases must execute and pass.'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Untouched Base: {} original JUnit cases passed; frozen={}'.format(len(data['observed']), args.freeze))
