FROM docker.io/library/ubuntu:20.04@sha256:8feb4d8ca5354def3d8fce243717141ce31e2c428701f6682bd2fafe15388214

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID
ARG PYTHON_VERSION
ARG PYTHON_SHA256
ARG EXTRA_APT_PACKAGES
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN for attempt in 1 2 3; do \
      apt-get update \
      && apt-get install -y --no-install-recommends --fix-missing ca-certificates \
      && break; \
      test "$attempt" -lt 3 || exit 1; \
    done \
    && sed -i 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g; s|http://security.ubuntu.com|https://security.ubuntu.com|g' /etc/apt/sources.list \
    && for attempt in 1 2 3; do \
         apt-get update \
         && apt-get install -y --no-install-recommends --fix-missing \
            autoconf automake bison build-essential flex gfortran git gperf \
            liblzma-dev libmotif-dev libreadline-dev libtool libxml2-dev \
            libx11-dev libxext-dev libxinerama-dev libxmu-dev libxpm-dev libxt-dev \
            openjdk-11-jdk-headless pkg-config python3 python-is-python3 \
         && break; \
         test "$attempt" -lt 3 || exit 1; \
       done \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

LABEL benchmark.instance_id="${INSTANCE_ID}" \
      benchmark.base_commit="${BASE_COMMIT}" \
      org.opencontainers.image.source="https://github.com/MDSplus/mdsplus"

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

# This historical checkout requires bootstrap/Gperf and Motif for the complete
# official TreeShr integration test. Serial make avoids an upstream ordering race.
RUN mkdir -p /build \
    && cd /testbed \
    && ./bootstrap \
    && cd /build \
    && NOF77=yes /testbed/configure --prefix=/usr/local/mdsplus --disable-java \
    && make \
    && make install \
    && groupadd --gid 64 benchmark \
    && useradd --uid 64 --gid 64 --create-home --shell /bin/bash benchmark \
    && chown -R benchmark:benchmark /testbed /build /usr/local/mdsplus \
    && runuser -u benchmark -- env HOME=/home/benchmark \
         PATH=/build/bin:/usr/local/mdsplus/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
         LD_LIBRARY_PATH=/build/lib \
         make -C /build/tditest/testing check TESTS=test-tdishr.tdi \
    && runuser -u benchmark -- env HOME=/home/benchmark \
         PATH=/build/bin:/usr/local/mdsplus/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
         LD_LIBRARY_PATH=/build/lib \
         make -C /build/tditest/testing check TESTS=test-treeshr.tdi \
    && runuser -u benchmark -- git -C /testbed reset --hard "${BASE_COMMIT}" \
    && runuser -u benchmark -- git -C /testbed clean -fdx \
    && test -z "$(runuser -u benchmark -- git -C /testbed status --porcelain)" \
    && mkdir -p /benchmark /inputs /results \
    && chown -R benchmark:benchmark /benchmark /inputs /results

ENV PATH=/usr/local/mdsplus/bin:${PATH} \
    LD_LIBRARY_PATH=/usr/local/mdsplus/lib \
    MDSPLUS_DIR=/usr/local/mdsplus \
    HOME=/home/benchmark
USER benchmark
WORKDIR /testbed
CMD ["/bin/bash"]

