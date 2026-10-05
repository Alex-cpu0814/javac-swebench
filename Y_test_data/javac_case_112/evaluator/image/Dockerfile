FROM mcr.microsoft.com/devcontainers/base:bookworm@sha256:3aacff4130e6cf04709f9cab1d7a6d3e1cc4bff6202bc61611831a18d3755673

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates cmake curl default-jdk-headless g++-multilib gcc-multilib \
       git make python3 python-is-python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}" \
      org.opencontainers.image.source="https://github.com/uclouvain/openjpeg"

RUN git clone --no-checkout "${REPO_URL}" /testbed \
    && cd /testbed \
    && git checkout --detach "${BASE_COMMIT}" \
    && git remote remove origin \
    && git config core.autocrlf false \
    && git for-each-ref --format='delete %(refname)' refs/heads refs/remotes refs/tags | git update-ref --stdin \
    && git reflog expire --expire=now --all \
    && git gc --prune=now \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)"

RUN mkdir -p /opt/openjpeg-data/input/nonregression \
    && touch /opt/openjpeg-data/README-OPJ-Data \
    && curl --fail --location --retry 3 \
       https://raw.githubusercontent.com/uclouvain/openjpeg-data/68b30b7f390b852106fb5ee2cf1dbc8628a2feaf/input/nonregression/issue571.tif \
       --output /opt/openjpeg-data/input/nonregression/issue571.tif \
    && echo '1c9dcd1801aac971759da985661bf074beb4c3a19c6ac4dbd8a0775f7f018e44  /opt/openjpeg-data/input/nonregression/issue571.tif' | sha256sum -c -

RUN cmake -S /testbed -B /opt/openjpeg-build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_C_FLAGS=-m32 \
        -DCMAKE_EXE_LINKER_FLAGS=-m32 \
        -DCMAKE_SHARED_LINKER_FLAGS=-m32 \
        -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
        -DBUILD_SHARED_LIBS=OFF \
        -DBUILD_CODEC=ON \
        -DBUILD_THIRDPARTY=ON \
        -DBUILD_TESTING=OFF \
    && cmake --build /opt/openjpeg-build --parallel "$(nproc)" \
    && mkdir -p /benchmark /inputs /results

WORKDIR /testbed
CMD ["/bin/bash"]
