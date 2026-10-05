FROM docker.io/library/maven:3.9.9-eclipse-temurin-17@sha256:f58d59b6273e785ac0a4477f6e9b5ba1d7731c75b906c0f7b34076f1851318cc

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential clang git python3 python-is-python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

LABEL benchmark.instance_id="${INSTANCE_ID}" \
      benchmark.base_commit="${BASE_COMMIT}" \
      org.opencontainers.image.source="https://github.com/kohlschutter/junixsocket"

RUN git init /testbed \
    && cd /testbed \
    && git remote add origin "${REPO_URL}" \
    && git fetch --depth 1 origin "${BASE_COMMIT}" \
    && git checkout --detach FETCH_HEAD \
    && git remote remove origin \
    && git config core.autocrlf false \
    && git for-each-ref --format='delete %(refname)' refs/remotes refs/tags | git update-ref --stdin \
    && git reflog expire --expire=now --all \
    && git gc --prune=now \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}"

# Warm all historical Maven/plugin dependencies, then remove project artifacts
# so every evaluation rebuilds the candidate's JNI library from source.
RUN cd /testbed \
    && mvn -B -Puse-snapshots,release-native \
       -pl junixsocket-native-custom -am clean install -DskipTests \
       -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
       -Djunixsocket.custom.shaded=default \
    && mvn -B -Puse-snapshots -pl junixsocket-common -am test \
       '-Dtest=AFUNIXSocketAddressTest' -Dsurefire.failIfNoSpecifiedTests=false \
    && rm -rf /root/.m2/repository/com/kohlschutter/junixsocket \
    && git clean -fdx \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results

WORKDIR /testbed
CMD ["/bin/bash"]
