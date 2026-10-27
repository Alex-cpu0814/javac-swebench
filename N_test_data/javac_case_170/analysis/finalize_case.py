"""Finalize verified records, checksum all release files, and validate the layout."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--docker', default='docker')
args = parser.parse_args()
subprocess.run([sys.executable, str(ROOT / 'analysis/verify_controls.py'), '--docker', args.docker], check=True)
subprocess.run([sys.executable, str(ROOT / 'analysis/write_records.py'), '--verified'], check=True)
config = json.loads((ROOT / 'evaluator/case_config.json').read_text(encoding='utf-8'))
final = json.loads((ROOT / 'verification/final_summary.json').read_text(encoding='utf-8'))
assert final['status'] == 'verified'
provenance = json.loads((ROOT / 'analysis/patch_provenance.json').read_text(encoding='utf-8'))
assert provenance['base_commit'] == config['base_commit'] and provenance['fix_commit'] == config['fix_commit']
assert provenance['exact_upstream_diff_sha256'] == hashlib.sha256((ROOT / 'patches/gold_patch.diff').read_bytes()).hexdigest()
official = ROOT / 'official_swebench'
manifest = official / 'SHA256SUMS.txt'
entries = []
for path in sorted(ROOT.rglob('*')):
    relative = path.relative_to(ROOT)
    if not path.is_file() or path == manifest:
        continue
    if relative.parts[:2] == ('analysis', 'work') or relative.parts[:3] == ('evaluator', 'image', 'context'):
        continue
    if '__pycache__' in relative.parts or '.git' in relative.parts:
        continue
    name = '../' + relative.as_posix()
    entries.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + name)
manifest.write_text('\n'.join(entries) + '\n', encoding='utf-8', newline='\n')
validator = ROOT.parents[1] / 'tools/validate_case_layout.py'
spec = importlib.util.spec_from_file_location('case_layout_validator', validator)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
errors = module.validate_case(ROOT)
assert not errors, errors
print('FINALIZED: {} SHA256 entries; standard layout and synchronized records validated.'.format(len(entries)))
