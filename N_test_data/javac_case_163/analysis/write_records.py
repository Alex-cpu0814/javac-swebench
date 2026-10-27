"""Write synchronized SWE-bench records; verification is populated from real runs."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = '90716d6008c5c9cfa8a061f3d23531acaea29777'
FIX = '77a4f0c8cd641fc5dfcb62922981c32393c8e079'
INSTANCE = 'kohlschutter__junixsocket-81'
F2P = ['org.newsclub.net.unix.Issue81CompatibilityTest.testAutomaticFallbackOldGlibc']
upstream = json.loads((ROOT / 'evaluator/upstream_tests.json').read_text(encoding='utf-8'))
P2P = ['org.newsclub.net.unix.Issue81CompatibilityTest.testModernGlibcRoundTrip'] + upstream['test_ids']
parser = argparse.ArgumentParser()
parser.add_argument('--verified', action='store_true')
args = parser.parse_args()
statement = '''junixsocket can terminate the JVM when binding a Unix-domain socket on Linux with an older glibc.

On x86_64 systems with glibc 2.12, the normal packaged native library can fail to load because it requires GLIBC_2.14. The library loader then falls back to its nodeps variant. Calling AFUNIXServerSocket.bind() subsequently terminates Java with a native dynamic-linker error:

java: symbol lookup error: ...libjunixsocket-native-2.3.2.so: undefined symbol: stat

This is the issue reported for multiple releases in #81 (the title names 2.2.0; this checkout reports version 2.3.2). The same application works on newer glibc systems.

Fix the native compatibility problem so the normal automatic library-loading path supports binding, connecting, exchanging data in both directions, and closing Unix-domain sockets on the older system. Preserve existing behavior on supported newer systems. Do not require application users to provide a preload workaround or replace the native socket implementation.
'''
test_file = 'junixsocket-common/src/test/java/org/newsclub/net/unix/Issue81GlibcProbe.java'
gold = (ROOT / 'patches/gold_patch.diff').read_text(encoding='utf-8')
test = (ROOT / 'patches/test_patch.diff').read_text(encoding='utf-8')
verification = {
    'docker_verified': args.verified, 'model_evaluator_verified': args.verified,
    'base_fails': args.verified, 'fix_passes': args.verified,
    'status': 'resolved' if args.verified else 'pending',
    'evaluation_assets_injected_at_runtime': True, 'image_contains_test_patch': False,
    'image_contains_gold_patch': False, 'image_contains_fix_commit': False,
    'model_evaluator_verification_type': 'isolated_base_gold_mutation_and_tamper_controls',
}
if args.verified:
    evidence = json.loads((ROOT / 'verification/final_summary.json').read_text(encoding='utf-8'))
    assert evidence['status'] == 'verified'
    assert evidence['test_patch_sha256'] == hashlib.sha256((ROOT / 'patches/test_patch.diff').read_bytes()).hexdigest()
instance = {
    'instance_id': INSTANCE, 'repo': 'kohlschutter/junixsocket', 'base_commit': BASE,
    'patch': gold, 'test_patch': test, 'problem_statement': statement, 'hints_text': '',
    'created_at': '2020-07-24', 'version': '2.3.2', 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS': P2P,
    'fix_commit': FIX, 'issue_url': 'https://github.com/kohlschutter/junixsocket/issues/81',
    'test_files': [test_file],
}
metadata = {
    'dataset_schema_version': '1.0', 'source_case': '163',
    'dataset_variant': 'SWE-bench-compatible custom record',
    'instance_id': INSTANCE, 'repo': instance['repo'], 'base_commit': BASE, 'fix_commit': FIX,
    'issue_url': instance['issue_url'], 'project_version': '2.3.2',
    'test_source': 'synthetic_issue_81_child_jvm_plus_unchanged_upstream_junit',
    'test_files': [test_file], 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS': P2P,
    'PASS_TO_PASS_COUNT': len(P2P), 'upstream_test_count': len(upstream['test_ids']),
    'excluded_upstream_test_ids': upstream['excluded_ids'],
    'excluded_upstream_test_reason': upstream['exclusion_reason'],
    'standard_layout': {'schema_version': '2.0', 'case_directory': 'javac_case_163',
        'analysis': 'analysis/', 'patches': 'patches/', 'official_swebench': 'official_swebench/',
        'evaluator': 'evaluator/', 'verification': 'verification/'},
    'verification': verification,
    'patch_provenance': {
        'gold_patch_authorship': 'kohlschutter/junixsocket_upstream',
        'gold_patch_source': 'exact_complete_upstream_fix_commit',
        'test_patch_source': 'synthetic_regression_derived_from_issue_81',
        'test_patch_authorship': 'dataset_construction',
        'upstream_regression_test_added_by_fix': False,
        'original_junit_tests_modified': False,
        'model_patch_example_source': 'copy_of_upstream_gold_for_evaluator_smoke_test',
        'model_patch_example_is_model_generated': False,
    },
    'model_evaluator_image': json.loads((ROOT / 'evaluator/case_config.json').read_text(encoding='utf-8'))['image'],
    'build_scope': 'core_Java_and_JNI_source_adapter_using_candidate_native_POM_and_AOL_options; full_Maven_packaging_not_claimed',
}
public = {key: instance[key] for key in ('instance_id', 'repo', 'base_commit', 'problem_statement',
                                       'hints_text', 'created_at', 'version', 'issue_url')}
source = {
    'instance_id': INSTANCE, 'source_case': '163', 'language_pair': 'Java-C',
    'repo': instance['repo'], 'base_commit': BASE, 'fix_commit': FIX,
    'commit_url': 'https://github.com/kohlschutter/junixsocket/commit/' + FIX,
    'issue_url': instance['issue_url'], 'problem_statement': statement,
    'test_source': metadata['test_source'], 'test_files': [test_file],
    'FAIL_TO_PASS': F2P, 'PASS_TO_PASS_COUNT': len(P2P),
    'verification_status': verification['status'], 'source_selection': 'user_provided_commit',
}
environment = {
    'instance_id': INSTANCE, 'task_level': 'integration',
    'validation_type': 'real_automatic_loader_child_jvm_and_upstream_junit',
    'environment': 'Linux_x86_64_glibc_2_23_build_and_QEMU_glibc_2_12_runtime',
    'python_version_target': '3.5+', 'java_requirement': 'AdoptOpenJDK 8u292',
    'build_system': metadata['build_scope'], 'test_execution': 'runtime_injected_case_adapter',
    'runtime_verified': args.verified, 'reproduction_status': verification['status'],
    'base_commit': BASE, 'fix_commit': FIX, 'test_source': metadata['test_source'],
    'test_files': [test_file], 'FAIL_TO_PASS': F2P, 'PASS_TO_PASS_COUNT': len(P2P),
    'verification': verification,
}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


official = ROOT / 'official_swebench'
write(official / 'instance_163.json', instance)
(official / 'instance_163.jsonl').write_text(json.dumps(instance, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
write(official / 'metadata.json', metadata)
write(official / 'public_task_163.json', public)
write(ROOT / 'analysis/source_row_163.json', source)
write(ROOT / 'analysis/environment_spec.json', environment)
shutil.copyfile(ROOT / 'patches/gold_patch.diff', ROOT / 'evaluator/model_patch_example.patch')


def modified(path, old, new):
    assert old.count(new) == 0 if new not in old else True
    before = (ROOT / 'analysis/work/base-only' / path).read_text(encoding='utf-8')
    assert before.count(old) == 1
    after = before.replace(old, new, 1)
    return ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
        fromfile='a/' + path, tofile='b/' + path))


controls = ROOT / 'verification/controls'
controls.mkdir(exist_ok=True)
if not (ROOT / 'analysis/work/base-only').is_dir():
    names = ('negative.patch', 'test_tamper.patch', 'upstream_tamper.patch',
             'port_regression.patch', 'alternative_nodeps_fix.patch')
    assert all((controls / name).is_file() for name in names), 'Missing frozen control patches'
    print('Updated records; retained frozen controls without regenerable Base cache.')
    raise SystemExit(0)
(controls / 'negative.patch').write_text('diff --git a/benchmark_negative_marker.txt b/benchmark_negative_marker.txt\nnew file mode 100644\n--- /dev/null\n+++ b/benchmark_negative_marker.txt\n@@ -0,0 +1 @@\n+negative-control\n', encoding='utf-8')
(controls / 'test_tamper.patch').write_text('diff --git a/{0} b/{0}\nnew file mode 100644\n--- /dev/null\n+++ b/{0}\n@@ -0,0 +1 @@\n+// candidate-created protected test\n'.format(test_file), encoding='utf-8')
path = 'junixsocket-common/src/test/java/org/newsclub/net/unix/AFUNIXSocketAddressTest.java'
before = (ROOT / 'analysis/work/base-only' / path).read_text(encoding='utf-8')
tamper = ''.join(difflib.unified_diff(before.splitlines(True), (before + '\n// candidate modification\n').splitlines(True), fromfile='a/' + path, tofile='b/' + path))
(controls / 'upstream_tamper.patch').write_text(gold + tamper, encoding='utf-8')
path = 'junixsocket-common/src/main/java/org/newsclub/net/unix/AFUNIXSocketAddress.java'
port_regression = modified(path, 'NativeUnixSocket.setPort1(this, port);', 'NativeUnixSocket.setPort1(this, port + 1);')
(controls / 'port_regression.patch').write_text(gold + port_regression, encoding='utf-8')
path = 'junixsocket-native/src/main/c/org_newsclub_net_unix_NativeUnixSocket.c'
alternate = modified(path, 'typedef enum {\n    kExceptionSocketException = 0,',
    '#if __GLIBC__ && __CROSSCLANG_NODEPS__\n# define stat(...) __xstat(1, __VA_ARGS__)\n#endif\n\ntypedef enum {\n    kExceptionSocketException = 0,')
(controls / 'alternative_nodeps_fix.patch').write_text(alternate, encoding='utf-8')
print('Wrote synchronized records: 1 FAIL_TO_PASS + {} PASS_TO_PASS ({} unchanged upstream).'.format(len(P2P), len(upstream['test_ids'])))
