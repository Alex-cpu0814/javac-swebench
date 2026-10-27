"""Synchronize private SWE-bench records and the public problem-only task."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'evaluator/case_config.json').read_text())
BASE, FIX, INSTANCE = (CONFIG[x] for x in ('base_commit', 'fix_commit', 'instance_id'))
upstream = json.loads((ROOT / 'evaluator/upstream_tests.json').read_text())
F2P = ['benchmark.noexec.noexec_home_fallback', 'benchmark.noexec.noexec_cwd_fallback']
P2P = ['benchmark.noexec.exec_loading', 'benchmark.noexec.all_noexec_rejected'] + upstream['test_ids']
parser = argparse.ArgumentParser()
parser.add_argument('--verified', action='store_true')
args = parser.parse_args()
statement = '''junixsocket cannot initialize its native socket implementation on Linux when its temporary directory is mounted noexec, even though another writable directory permits loading native libraries.

Issue #140 reports the problem with junixsocket 2.7.2 and 2.8.0 on RHEL 9.2. With a noexec temporary directory, extracting a shared library can succeed while System.load fails with an UnsatisfiedLinkError, for example "failed to map segment from shared object". Subsequent socket operations fail because the native implementation was not initialized.

Fix automatic native-library loading so it can recover from an unsuccessful temporary-directory load using the existing alternate writable locations. It should also recover when both the temporary directory and the home directory prohibit execution but the working directory permits loading. Do not require application users to disable security controls or supply a manual library override. Preserve normal loading and real Unix-domain socket I/O; when every location prohibits loading, initialization must still fail rather than reporting success.
'''
gold = (ROOT / 'patches/gold_patch.diff').read_text(encoding='utf-8')
test = (ROOT / 'patches/test_patch.diff').read_text(encoding='utf-8')
test_file = 'benchmark-tests/org/newsclub/net/unix/NoexecProbe.java'
verification = {'docker_verified': args.verified, 'model_evaluator_verified': args.verified,
    'base_fails': args.verified, 'fix_passes': args.verified,
    'status': 'resolved' if args.verified else 'pending',
    'evaluation_assets_injected_at_runtime': True, 'image_contains_test_patch': False,
    'image_contains_gold_patch': False, 'image_contains_fix_commit': False,
    'model_evaluator_verification_type': 'isolated_base_gold_alternative_regression_and_tamper_controls'}
if args.verified:
    evidence = json.loads((ROOT / 'verification/final_summary.json').read_text())
    assert evidence['status'] == 'verified'
    assert evidence['test_patch_sha256'] == hashlib.sha256((ROOT / 'patches/test_patch.diff').read_bytes()).hexdigest()
instance = {'instance_id': INSTANCE, 'repo': 'kohlschutter/junixsocket', 'base_commit': BASE,
    'patch': gold, 'test_patch': test, 'problem_statement': statement, 'hints_text': '',
    'created_at': '2023-09-29', 'version': '2.8.1-SNAPSHOT', 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS': P2P,
    'fix_commit': FIX, 'issue_url': 'https://github.com/kohlschutter/junixsocket/issues/140', 'test_files': [test_file]}
scope = 'candidate_core_Java8_source_build_with_pinned_official_2.8.0_JNI_runtime_fixture; not_full_Maven_or_native_source_rebuild'
metadata = {'dataset_schema_version': '1.0', 'source_case': '170',
    'dataset_variant': 'SWE-bench-compatible custom record', 'instance_id': INSTANCE,
    'repo': instance['repo'], 'base_commit': BASE, 'fix_commit': FIX, 'issue_url': instance['issue_url'],
    'project_version': instance['version'], 'test_source': 'synthetic_issue140_real_noexec_and_unchanged_upstream_JUnit',
    'test_files': [test_file], 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS': P2P, 'PASS_TO_PASS_COUNT': len(P2P),
    'upstream_test_count': len(upstream['test_ids']), 'upstream_selected_classes': upstream['selected_classes'],
    'standard_layout': {'schema_version': '2.0', 'case_directory': 'javac_case_170',
                        **{x: x + '/' for x in ('analysis', 'patches', 'official_swebench', 'evaluator', 'verification')}},
    'verification': verification, 'patch_provenance': {
        'gold_patch_authorship': 'kohlschutter/junixsocket_upstream',
        'gold_patch_source': 'exact_complete_upstream_fix_commit',
        'test_patch_authorship': 'dataset_construction', 'test_patch_source': 'synthetic_regression_derived_from_issue140',
        'upstream_regression_test_added_by_fix': False, 'original_junit_tests_modified': False,
        'model_patch_example_source': 'copy_of_upstream_gold_for_evaluator_smoke_test',
        'model_patch_example_is_model_generated': False, 'fix_visible_during_test_design': True},
    'model_evaluator_image': CONFIG['image'], 'build_scope': scope,
    'limitations': ['Linux noexec mechanism reproduced; not a complete RHEL SELinux policy replica',
                    'Java 8 core source adapter; Java 15/multi-module Maven packaging and candidate native C changes are outside grading scope',
                    'Selected upstream classes are a scoped regression suite, not the entire project suite']}
public = {k: instance[k] for k in ('instance_id', 'repo', 'base_commit', 'problem_statement',
                                  'hints_text', 'created_at', 'version', 'issue_url')}
source = {'instance_id': INSTANCE, 'source_case': '170', 'language_pair': 'Java-C',
    'repo': instance['repo'], 'base_commit': BASE, 'fix_commit': FIX,
    'commit_url': 'https://github.com/kohlschutter/junixsocket/commit/' + FIX,
    'issue_url': instance['issue_url'], 'problem_statement': statement, 'test_source': metadata['test_source'],
    'test_files': [test_file], 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS_COUNT': len(P2P),
    'verification_status': verification['status'], 'source_selection': 'user_provided_commit'}
environment = {'instance_id': INSTANCE, 'task_level': 'integration',
    'validation_type': 'real_noexec_tmpfs_child_JVM_native_socket_roundtrip_and_upstream_JUnit',
    'environment': 'Linux_x86_64_Ubuntu22.04_glibc2.35', 'python_version_target': '3.10+',
    'java_requirement': 'Temurin 8u504', 'build_system': scope,
    'test_execution': 'runtime_injected_case_adapter_with_exec_and_noexec_Docker_tmpfs',
    'runtime_verified': args.verified, 'reproduction_status': verification['status'],
    'base_commit': BASE, 'fix_commit': FIX, 'test_source': metadata['test_source'],
    'test_files': [test_file], 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS_COUNT': len(P2P), 'verification': verification}
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
official = ROOT / 'official_swebench'
write(official / 'instance_170.json', instance)
(official / 'instance_170.jsonl').write_text(json.dumps(instance, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
write(official / 'metadata.json', metadata)
write(official / 'public_task_170.json', public)
write(ROOT / 'analysis/source_row_170.json', source)
write(ROOT / 'analysis/environment_spec.json', environment)
shutil.copyfile(ROOT / 'patches/gold_patch.diff', ROOT / 'evaluator/model_patch_example.patch')
controls = ROOT / 'verification/controls'
controls.mkdir(exist_ok=True)
if not (ROOT / 'analysis/work/base-only').is_dir():
    names = ('negative.patch', 'test_tamper.patch', 'upstream_tamper.patch',
             'port_regression.patch', 'alternative_fix.patch')
    assert all((controls / name).is_file() for name in names), 'Missing frozen control patches'
    print('Updated records; retained frozen controls without regenerable Base cache.')
    raise SystemExit(0)
def modified(path, old, new):
    before = (ROOT / 'analysis/work/base-only' / path).read_text(encoding='utf-8')
    assert before.count(old) == 1, path
    after = before.replace(old, new, 1)
    return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/' + path, tofile='b/' + path))
(controls / 'negative.patch').write_text('diff --git a/benchmark_negative_marker.txt b/benchmark_negative_marker.txt\nnew file mode 100644\n--- /dev/null\n+++ b/benchmark_negative_marker.txt\n@@ -0,0 +1 @@\n+negative-control\n', encoding='utf-8')
(controls / 'test_tamper.patch').write_text('diff --git a/{0} b/{0}\nnew file mode 100644\n--- /dev/null\n+++ b/{0}\n@@ -0,0 +1 @@\n+// candidate-created protected test\n'.format(test_file), encoding='utf-8')
path = 'junixsocket-common/src/test/java/org/newsclub/net/unix/AFUNIXSocketAddressTest.java'
before = (ROOT / 'analysis/work/base-only' / path).read_text(encoding='utf-8')
tamper = ''.join(difflib.unified_diff(before.splitlines(True), (before + '\n// candidate modification\n').splitlines(True), fromfile='a/' + path, tofile='b/' + path))
(controls / 'upstream_tamper.patch').write_text(gold + tamper, encoding='utf-8')
path = 'junixsocket-common/src/main/java/org/newsclub/net/unix/AFSocketAddress.java'
(controls / 'port_regression.patch').write_text(gold + modified(path,
    'NativeUnixSocket.setPort1(addr, port);', 'NativeUnixSocket.setPort1(addr, port + 1);'), encoding='utf-8')
path = 'junixsocket-common/src/main/java/org/newsclub/net/unix/NativeLibraryLoader.java'
alternate = modified(path,
    '          String message = e.getMessage().toLowerCase(Locale.getDefault());\n'
    '          if (!message.contains("perm")) {',
    '          // Exhaust the three configured locations independently of diagnostic text.\n'
    '          if (attempt == 2) {')
(controls / 'alternative_fix.patch').write_text(alternate, encoding='utf-8')
print('Wrote records: {} FAIL_TO_PASS + {} PASS_TO_PASS ({} upstream).'.format(len(F2P), len(P2P), len(upstream['test_ids'])))
