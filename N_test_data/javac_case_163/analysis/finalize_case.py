"""Finalize synchronized records, full checksums, and targeted layout checks."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
record = json.loads((ROOT / 'verification/final_summary.json').read_text(encoding='utf-8'))
assert record['status'] == 'verified'
build = json.loads((ROOT / 'verification/builds/case-163-build-final/summary.json').read_text(encoding='utf-8'))
assert build['status'] == 'success' and build['image']['id'] == record['image_id']
for name, expected in record['evaluation_assets_sha256'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected
for value in record['controls'].values():
    path = ROOT / 'verification' / value['summary']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == value['summary_sha256']
subprocess.run([sys.executable, str(ROOT / 'analysis/write_records.py'), '--verified'], check=True)
ignored = ('evaluator/image/context/', 'analysis/work/', 'analysis/upstream_discovery/testclasses/')
manifest = ROOT / 'official_swebench/SHA256SUMS.txt'
entries = []
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or path == manifest:
        continue
    name = path.relative_to(ROOT).as_posix()
    if name.startswith(ignored) or '__pycache__' in path.parts or path.suffix == '.pyc':
        continue
    target = path.relative_to(ROOT / 'official_swebench').as_posix() if path.parent == ROOT / 'official_swebench' else '../' + name
    entries.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + target)
manifest.write_text('\n'.join(entries) + '\n', encoding='utf-8', newline='\n')
sys.path.insert(0, str(REPO))
from tools.validate_case_layout import validate_case
errors = validate_case(ROOT)
assert not errors, errors
print('Finalized case 163; {} checksums and targeted layout validation passed.'.format(len(entries)))
