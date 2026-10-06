FROM docker.io/library/maven:3.9.9-eclipse-temurin-17-focal@sha256:45ddc84a2e7f75ab7faf290085a0292dd8adc5e7674a89231f6a879b60f4358d

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN for attempt in 1 2 3; do \
      apt-get update \
      && apt-get install -y --no-install-recommends --fix-missing \
         build-essential clang git python3 python-is-python3 \
      && break; \
      test "$attempt" -lt 3 || exit 1; \
    done \
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

# Warm the native build, Jetty test dependencies, and the stable control.
# Project-owned artifacts are removed so every evaluation rebuilds the source.
RUN cd /testbed \
    && for attempt in 1 2 3; do \
         mvn -B -Prelease-native \
           -pl junixsocket-native-custom,junixsocket-jetty -am clean install \
           -DskipTests \
           -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
           -Djunixsocket.custom.shaded=default \
         && break; \
         test "$attempt" -lt 3 || exit 1; \
       done \
    && mvn -B -f junixsocket-jetty/pom.xml test \
       '-Dtest=UnixDomainTest#testHTTPOverUnixDomain' \
    && rm -rf /root/.m2/repository/com/kohlschutter/junixsocket \
    && git clean -fdx \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results

WORKDIR /testbed
CMD ["/bin/bash"]
