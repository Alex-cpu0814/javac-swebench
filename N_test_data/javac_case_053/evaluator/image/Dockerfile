FROM public.ecr.aws/docker/library/ubuntu:22.04@sha256:5ec03bb3441e8b0bf3b4f9cd4629a1ae763010dc3035bb8da3ae6cf026486401
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    clang-14 openjdk-17-jdk-headless python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV CC=clang-14
WORKDIR /workspace

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/local/bin/python
LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}"
RUN git init /testbed && cd /testbed \
    && git config core.autocrlf false \
    && git remote add origin "${REPO_URL}" \
    && git fetch --depth=1 origin "${BASE_COMMIT}" \
    && git checkout --detach FETCH_HEAD \
    && git remote remove origin \
    && rm -f .git/FETCH_HEAD .git/ORIG_HEAD \
    && git for-each-ref --format='delete %(refname)' refs/heads refs/remotes refs/tags | git update-ref --stdin \
    && git reflog expire --expire=now --all && git gc --prune=now \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results
WORKDIR /testbed
CMD ["/bin/bash"]
