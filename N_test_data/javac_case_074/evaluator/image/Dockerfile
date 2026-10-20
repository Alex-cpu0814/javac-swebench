FROM eclipse-temurin:8-jdk-jammy

RUN apt-get update \
    && apt-get install -y --no-install-recommends git python3 gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

ARG BASE_COMMIT
ARG INSTANCE_ID
LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}" \
      org.opencontainers.image.source="https://github.com/LWJGL/lwjgl3"
WORKDIR /testbed
ADD base-git.tar.gz /testbed/.git/
RUN git config core.bare false \
    && git config core.autocrlf false \
    && git checkout --detach "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results

CMD ["/bin/bash"]
