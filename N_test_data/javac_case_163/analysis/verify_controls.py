"""Run and validate Base, Gold, alternative-fix, regression, and tamper controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--docker', required=True)
parser.add_argument('--suffix', default='published')
parser.add_argument('--reuse-existing', action='store_true')
args = parser.parse_args()
config = json.loads((ROOT / 'evaluator/case_config.json').read_text(encoding='utf-8'))
instance = json.loads((ROOT / config['instance_file']).read_text(encoding='utf-8'))
image = json.loads(subprocess.check_output([args.docker, 'image', 'inspect', config['image']]))[0]['Id']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


asset_names = [a['source'] for a in config['runtime_assets']] + [
    'evaluator/run_evaluation.sh', 'evaluator/case_config.json',
    'evaluator/evaluate_model_patch.py', 'evaluator/logging_v3.py']
assets = {name: digest(ROOT / name) for name in asset_names}
cases = [
    ('tamper', 'verification/controls/test_tamper.patch'),
    ('upstream-tamper', 'verification/controls/upstream_tamper.patch'),
    ('port-regression', 'verification/controls/port_regression.patch'),
    ('alternative', 'verification/controls/alternative_nodeps_fix.patch'),
    ('base', 'verification/controls/negative.patch'),
    ('gold', 'patches/gold_patch.diff'),
]
validated = {}
for label, patch in cases:
    run_id = 'case-163-' + label + '-' + args.suffix
    folder = ROOT / 'verification/runs' / run_id
    if folder.exists() and not args.reuse_existing:
        raise SystemExit('Run exists; use a new suffix or --reuse-existing: ' + run_id)
    if not folder.exists():
        result = subprocess.run([
            sys.executable, str(ROOT / 'evaluator/evaluate_model_patch.py'),
            '--patch', str(ROOT / patch), '--run-id', run_id, '--label', label,
            '--docker', args.docker,
        ], cwd=ROOT)
        assert result.returncode in (0, 1), (label, result.returncode)
    summary = json.loads((folder / 'summary.json').read_text(encoding='utf-8'))
    assert summary['model_patch_sha256'] == digest(ROOT / patch)
    assert summary['test_patch_sha256'] == digest(ROOT / 'patches/test_patch.diff')
    assert summary['evaluation_assets_sha256'] == assets
    assert summary['image']['id'] == image
    if label == 'tamper':
        assert summary['reason'] == 'candidate_conflicts_with_test_patch', summary
    elif label == 'upstream-tamper':
        assert summary['reason'] == 'project_build_failed'
        assert 'protected_upstream_test_modified' in (folder / 'project-build.raw.log').read_text(encoding='utf-8')
    else:
        grading = json.loads((folder / 'grading.json').read_text(encoding='utf-8'))
        assert grading['tests_observed'] == len(instance['FAIL_TO_PASS']) + len(instance['PASS_TO_PASS'])
        if label == 'base':
            assert summary['status'] == 'unresolved'
            assert set(grading['FAIL_TO_PASS'].values()) == {'FAILED'}
            assert set(grading['PASS_TO_PASS'].values()) == {'PASSED'}
            assert 'undefined symbol: stat' in (folder / 'children/old-glibc.stderr.log').read_text(encoding='utf-8')
            child = json.loads((folder / 'children/old-glibc.json').read_text(encoding='utf-8'))
            assert child['exit_code'] == 127 and not child['timed_out']
        elif label == 'port-regression':
            assert set(grading['FAIL_TO_PASS'].values()) == {'PASSED'}
            failed = [name for name, status in grading['PASS_TO_PASS'].items() if status != 'PASSED']
            assert failed == ['org.newsclub.net.unix.AFUNIXSocketAddressTest.testPort'], failed
        else:
            assert summary['status'] == 'resolved'
            assert set(grading['FAIL_TO_PASS'].values()) == {'PASSED'}
            assert set(grading['PASS_TO_PASS'].values()) == {'PASSED'}
    validated[label] = {'run_id': run_id, 'summary': 'runs/' + run_id + '/summary.json',
                        'status': summary['status'], 'reason': summary['reason'],
                        'summary_sha256': digest(folder / 'summary.json')}
    print('Validated ' + label + ': ' + summary['reason'], flush=True)
record = {'status': 'verified', 'test_patch_sha256': digest(ROOT / 'patches/test_patch.diff'),
          'image_id': image, 'evaluation_assets_sha256': assets,
          'fail_to_pass_count': len(instance['FAIL_TO_PASS']),
          'pass_to_pass_count': len(instance['PASS_TO_PASS']),
          'upstream_pass_to_pass_count': len(instance['PASS_TO_PASS']) - 1,
          'controls': validated}
(ROOT / 'verification/final_summary.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print('All six control outcomes verified.')
