FROM eclipse-temurin:8-jdk-jammy

RUN apt-get update \
    && apt-get install -y --no-install-recommends git python3 gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/benchmark/lib && set -eux; \
    version=3.2.0; \
    for artifact in lwjgl lwjgl-openvr; do \
      for classifier in '' '-natives-linux'; do \
        file="$artifact-$version$classifier.jar"; \
        curl -fsSL --retry 3 -o "/opt/benchmark/lib/$file" \
          "https://repo.maven.apache.org/maven2/org/lwjgl/$artifact/$version/$file"; \
      done; \
    done; \
    curl -fsSL --retry 3 -o /opt/benchmark/lib/jsr305.jar \
      https://repo.maven.apache.org/maven2/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar; \
    printf '%s\n' \
      '766ad2a0783f2687962c8ad74ceecc38a28b9f72a2d085ee438b7813e928d0c7  /opt/benchmark/lib/jsr305.jar' \
      '97af9a688081bbdf0cf208b93f02b58fe2db0504ee7333e54780c4b6f70694f8  /opt/benchmark/lib/lwjgl-3.2.0.jar' \
      '08ca6d394ef7ac97002bc939642dc285c7f61c94a69070fa9a916921fee637ab  /opt/benchmark/lib/lwjgl-3.2.0-natives-linux.jar' \
      '117a98d2ae5503f0af291ff84325f12eebfd3ea73941060e8181720840812143  /opt/benchmark/lib/lwjgl-openvr-3.2.0.jar' \
      '5144df18be5868ad4bb8b9ab5174275f860b4c34bd2b4f01539973f81a6fbb8b  /opt/benchmark/lib/lwjgl-openvr-3.2.0-natives-linux.jar' \
      | sha256sum -c -

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
