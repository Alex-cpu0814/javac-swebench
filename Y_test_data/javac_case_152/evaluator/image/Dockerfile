FROM docker.io/library/maven:3.9.9-eclipse-temurin-17-focal@sha256:45ddc84a2e7f75ab7faf290085a0292dd8adc5e7674a89231f6a879b60f4358d

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
ARG FIX_COMMIT=2f8f096b84fba1ae26058d41cc03df47719379df
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

# Warm dependencies used by the post-refactor tree in a temporary checkout.
# The checkout and all project-owned Maven artifacts are deleted in this same
# layer, so no fixed source, patch, or fix commit object remains in the image.
RUN git init /tmp/dependency-warmup \
    && cd /tmp/dependency-warmup \
    && git remote add origin "${REPO_URL}" \
    && git fetch --depth 1 origin "${FIX_COMMIT}" \
    && git checkout --detach FETCH_HEAD \
    && mvn -B -Prelease-native \
       -pl junixsocket-native-common,junixsocket-native-custom -am clean install \
       -Dmaven.test.skip=true \
       -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
       -Djunixsocket.custom.shaded=default \
    && mvn -B -f junixsocket-common/pom.xml package -Dmaven.test.skip=true \
    && cd / \
    && rm -rf /tmp/dependency-warmup \
    && rm -rf /root/.m2/repository/com/kohlschutter/junixsocket

# Warm Base dependencies separately. Evaluations rebuild every project artifact
# from the candidate source while Docker networking is disabled.
RUN cd /testbed \
    && mvn -B -Prelease-native \
       -pl junixsocket-native-common,junixsocket-native-custom -am clean install \
       -Dmaven.test.skip=true \
       -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
       -Djunixsocket.custom.shaded=default \
    && mvn -B -f junixsocket-common/pom.xml package -Dmaven.test.skip=true \
    && rm -rf /root/.m2/repository/com/kohlschutter/junixsocket \
    && git clean -fdx \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results

WORKDIR /testbed
CMD ["/bin/bash"]
