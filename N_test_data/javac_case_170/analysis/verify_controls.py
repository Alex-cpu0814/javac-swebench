"""Run/validate Base, Gold, alternative repair, regression, and protected-test controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--docker', default='docker')
parser.add_argument('--run-missing', action='store_true')
parser.add_argument('--revision', default='published-v1')
parser.add_argument('--build-run-id', default='build-170-published')
args = parser.parse_args()
config = json.loads((ROOT / 'evaluator/case_config.json').read_text())
instance = json.loads((ROOT / 'official_swebench/instance_170.json').read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
image = json.loads(subprocess.check_output([args.docker, 'image', 'inspect', config['image']]))[0]['Id']
controls = [('base', 'verification/controls/negative.patch'), ('gold', 'patches/gold_patch.diff'),
            ('alternative', 'verification/controls/alternative_fix.patch'),
            ('port-regression', 'verification/controls/port_regression.patch'),
            ('test-tamper', 'verification/controls/test_tamper.patch'),
            ('upstream-tamper', 'verification/controls/upstream_tamper.patch')]
records = {}
assets = {name: sha(ROOT / name) for name in ('evaluator/run_evaluation.sh', 'evaluator/case_config.json',
          'evaluator/evaluate_model_patch.py', 'evaluator/logging_v3.py')}
assets.update({entry['source']: sha(ROOT / entry['source']) for entry in config['runtime_assets']})
for label, patch in controls:
    run_id = label + '-170-' + args.revision
    out = ROOT / 'verification/runs' / run_id
    if not (out / 'summary.json').is_file() and args.run_missing:
        completed = subprocess.run([sys.executable, str(ROOT / 'evaluator/evaluate_model_patch.py'),
            '--patch', str(ROOT / patch), '--run-id', run_id, '--label', label, '--timeout', '420', '--docker', args.docker])
        assert completed.returncode in (0, 1), (label, completed.returncode)
    summary = read(out / 'summary.json')
    assert summary['model_patch_sha256'] == sha(ROOT / patch), label + ': patch changed after run'
    assert summary['test_patch_sha256'] == sha(ROOT / 'patches/test_patch.diff')
    assert summary['evaluation_assets_sha256'] == assets, label + ': evaluator changed after run'
    assert summary['image']['id'] == image
    assert summary['phase']['outcome'] != 'infrastructure_error'
    if label in ('base', 'gold', 'alternative', 'port-regression'):
        assert summary['phase']['phase'] == 'tests_complete'
        grading = read(out / 'grading.json')
        assert set(grading['FAIL_TO_PASS']) == set(instance['FAIL_TO_PASS'])
        assert set(grading['PASS_TO_PASS']) == set(instance['PASS_TO_PASS'])
        assert summary['grading']['tests_observed'] == len(instance['FAIL_TO_PASS']) + len(instance['PASS_TO_PASS'])
        assert all(x in ('PASSED', 'FAILED') for key in ('FAIL_TO_PASS', 'PASS_TO_PASS') for x in grading[key].values())
        if label == 'base':
            assert set(grading['FAIL_TO_PASS'].values()) == {'FAILED'}
            assert set(grading['PASS_TO_PASS'].values()) == {'PASSED'}
            assert summary['status'] == 'unresolved'
            for name in ('noexec_home_fallback', 'noexec_cwd_fallback'):
                text = (out / (name + '.raw.log')).read_text()
                lines = [line for line in text.splitlines() if 'UnsatisfiedLinkError' in line and 'failed to map segment from shared object' in line]
                assert lines and all('perm' not in line.lower() for line in lines)
                assert not read(out / (name + '.json'))['timeout']
        elif label == 'port-regression':
            assert set(grading['FAIL_TO_PASS'].values()) == {'PASSED'}
            assert all(grading['PASS_TO_PASS'][x] == 'PASSED' for x in ('benchmark.noexec.exec_loading', 'benchmark.noexec.all_noexec_rejected'))
            assert any(value == 'FAILED' and name.startswith('org.newsclub.') for name, value in grading['PASS_TO_PASS'].items())
            assert summary['status'] == 'unresolved'
        else:
            assert summary['status'] == 'resolved'
            assert all(value == 'PASSED' for key in ('FAIL_TO_PASS', 'PASS_TO_PASS') for value in grading[key].values())
    elif label == 'test-tamper':
        assert summary['status'] == 'unresolved'
        assert summary['phase']['reason'] == 'candidate_conflicts_with_test_patch'
    else:
        assert summary['status'] == 'unresolved' and summary['phase']['reason'] == 'project_build_failed'
        assert 'protected_upstream_test_modified:' in (out / 'project-build.raw.log').read_text()
    records[label] = {'run_id': run_id, 'status': summary['status'], 'phase': summary['phase'],
                      'grading': summary['grading'], 'model_patch_sha256': summary['model_patch_sha256'],
                      'summary_sha256': sha(out / 'summary.json')}
build = ROOT / 'verification/builds' / args.build_run_id
build_summary = read(build / 'summary.json')
assert build_summary['image_id'] == image and build_summary['status'] == 'built_and_audited'
assert build_summary['dockerfile_sha256'] == sha(ROOT / 'evaluator/image/Dockerfile')
assert build_summary['builder_sha256'] == sha(ROOT / 'evaluator/build_model_evaluator.py')
assert build_summary['audit_log_sha256'] == sha(build / 'image-audit.raw.log')
assert build_summary['context_sha256'] == read(ROOT / 'analysis/image_context.json')['assets']
evidence = {'status': 'verified', 'instance_id': instance['instance_id'], 'image_id': image,
            'FAIL_TO_PASS_COUNT': len(instance['FAIL_TO_PASS']), 'PASS_TO_PASS_COUNT': len(instance['PASS_TO_PASS']),
            'upstream_junit_count': len(read(ROOT / 'evaluator/upstream_tests.json')['test_ids']),
            'gold_patch_sha256': sha(ROOT / 'patches/gold_patch.diff'),
            'test_patch_sha256': sha(ROOT / 'patches/test_patch.diff'),
            'evaluation_assets_sha256': assets, 'controls': records,
            'image_build_summary_sha256': sha(build / 'summary.json'),
            'limitations': read(ROOT / 'official_swebench/metadata.json')['limitations']}
(ROOT / 'verification/final_summary.json').write_text(json.dumps(evidence, indent=2) + '\n')
print('VERIFIED: 6 controls; Base 2 failures/{} preserved; Gold and equivalent alternative {}/{}.'.format(
      len(instance['PASS_TO_PASS']), len(instance['PASS_TO_PASS']) + 2, len(instance['PASS_TO_PASS']) + 2))
