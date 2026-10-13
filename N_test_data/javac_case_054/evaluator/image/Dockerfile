FROM ubuntu:22.04@sha256:5ec03bb3441e8b0bf3b4f9cd4629a1ae763010dc3035bb8da3ae6cf026486401
ENV DEBIAN_FRONTEND=noninteractive JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends ant ca-certificates git openjdk-17-jdk-headless gcc g++ libx11-dev make unzip python3 && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends libffi-dev=3.4.2-4 && apt-get clean && rm -rf /var/lib/apt/lists/* && ln -s /usr/bin/python3 /usr/local/bin/python

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
ARG PYTHON_VERSION
ARG PYTHON_SHA256
ARG EXTRA_APT_PACKAGES
LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}" org.opencontainers.image.source="https://github.com/LWJGL/lwjgl3"
WORKDIR /testbed
RUN git init && git -c http.proxy= fetch --depth=1 "${REPO_URL}" "${BASE_COMMIT}" && git checkout --detach FETCH_HEAD && git config core.autocrlf false

# Resolve Base-declared Java/Kotlin dependencies while image building has
# network access. Custom libffi is an explicit accepted PIC adaptation.
# The current project's JNI is compiled by standard Ant, never preinstalled.
RUN python3 - <<'PY'
import hashlib
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

assert subprocess.check_output(['uname', '-m'], text=True).strip() == 'x86_64'
names = sorted({e.attrib.get('name', e.attrib.get('property', '')) for e in ET.parse('config/build-bindings.xml').iter() if e.attrib.get('name', e.attrib.get('property', '')).startswith('binding.')} - {'binding.DISABLE_CHECKS'})
flags = ['-D' + name + '=' + ('true' if name == 'binding.vulkan' else 'false') for name in names]
subprocess.run(['ant', '-Dbuild.type=release/3.3.1', *flags, 'compile-templates'], check=True)
archive = Path('/usr/lib/x86_64-linux-gnu/libffi_pic.a')
assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'fe417849a4af3c711b6b94f45219fbeb788896aaab478dd1806ecc23a8cfb85e'
dest = Path('bin/libs/native/linux/x64/org/lwjgl/libffi.a')
dest.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(archive, dest)
subprocess.run(['ant', '-Dbuild.type=release/3.3.1', '-Dbuild.offline=true', *flags, 'compile-native'], check=True)
PY

# Return tracked inputs to exact Base; preserve cached products/dependencies.
# Shallow Base fetch contains no fixing commit, gold patch or test oracle.
RUN git restore --source="${BASE_COMMIT}" --worktree -- . \
    && git for-each-ref --format='delete %(refname)' refs/heads refs/remotes refs/tags | git update-ref --stdin
RUN git reflog expire --expire=now --all && git gc --prune=now \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results
CMD ["/bin/bash"]
