"""Recreate the Base-only image context without the exploratory case directory."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--repo-url', default='https://github.com/kohlschutter/junixsocket.git')
args = parser.parse_args()
config = json.loads((ROOT / 'evaluator/case_config.json').read_text(encoding='utf-8'))
context = ROOT / 'evaluator/image/context'
context.mkdir(exist_ok=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for asset in json.loads((ROOT / 'analysis/toolchain_assets.json').read_text(encoding='utf-8')):
    assert Path(asset['name']).name == asset['name']
    target = context / asset['name']
    if not target.exists():
        cached = ROOT.with_name('javac_case_163_new') / 'assets' / asset['name']
        if cached.is_file() and digest(cached) == asset['sha256']:
            shutil.copyfile(cached, target)
        else:
            print('Downloading public dependency: ' + asset['name'], flush=True)
            with urllib.request.urlopen(asset['url'], timeout=180) as response, target.open('wb') as output:
                shutil.copyfileobj(response, output)
    assert digest(target) == asset['sha256'], 'Dependency hash mismatch: ' + asset['name']

base = ROOT / 'analysis/work/base-only'
if not base.exists():
    base.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', str(base)], check=True)
    subprocess.run(['git', '-C', str(base), 'config', 'core.autocrlf', 'false'], check=True)
    subprocess.run(['git', '-C', str(base), 'fetch', '--depth=1', args.repo_url, config['base_commit']], check=True)
    subprocess.run(['git', '-C', str(base), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
assert subprocess.check_output(['git', '-C', str(base), 'rev-parse', 'HEAD']).decode().strip() == config['base_commit']
assert not subprocess.check_output(['git', '-C', str(base), 'status', '--porcelain']).strip()
assert subprocess.run(['git', '-C', str(base), 'cat-file', '-e', config['fix_commit']], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0
files = {p.relative_to(base).as_posix(): digest(p) for p in base.rglob('*')
         if p.is_file() and '.git' not in p.relative_to(base).parts}
expected = json.loads((ROOT / 'analysis/source_provenance.json').read_text(encoding='utf-8'))['sources']['base']['files']
assert files == expected, 'Base source fingerprint differs from canonical upstream Git objects'
with tarfile.open(context / 'base-source.tar', 'w') as archive:
    for path in sorted(base.rglob('*')):
        info = archive.gettarinfo(str(path), path.relative_to(base).as_posix())
        info.uid = info.gid = info.mtime = 0
        info.uname = info.gname = ''
        info.mode = 0o755 if path.is_dir() else 0o644
        if path.is_file():
            with path.open('rb') as handle:
                archive.addfile(info, handle)
        else:
            archive.addfile(info)
record = {'base_commit': config['base_commit'], 'fix_commit_absent': True,
          'assets': {p.name: digest(p) for p in sorted(context.iterdir()) if p.is_file()}}
(ROOT / 'analysis/image_context.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print('Prepared verified public dependencies and Base-only Git/source archive.')
