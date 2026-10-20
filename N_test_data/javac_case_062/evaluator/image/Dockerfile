FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && sed -i 's|http://archive.ubuntu.com|https://mirrors.aliyun.com|g; s|http://security.ubuntu.com|https://mirrors.aliyun.com|g' /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       ant git python3 openjdk-11-jdk-headless gcc g++ make libclang-14-dev libffi-dev \
    && ln -s /usr/bin/python3 /usr/local/bin/python \
    && test -r /usr/lib/llvm-14/lib/libclang.so \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends libx11-dev \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ARG BASE_COMMIT
ARG INSTANCE_ID
LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}" org.opencontainers.image.source="https://github.com/LWJGL/lwjgl3"
WORKDIR /testbed
ADD base-git.tar.gz /testbed/.git/
RUN git config core.bare false && git config core.autocrlf false \
    && git checkout --detach "${BASE_COMMIT}" && test -z "$(git status --porcelain)"
ADD dependency-cache.tar.gz /testbed/bin/libs/
ADD dyncall-source.tar.gz /opt/
COPY normalize_dyncall.py /tmp/normalize_dyncall.py
RUN python3 /tmp/normalize_dyncall.py && cd /opt/dyncall && ./configure && make -j2 \
    && mkdir -p /testbed/bin/libs/native/linux/x64/org/lwjgl \
    && cp dyncall/libdyncall_s.a dyncallback/libdyncallback_s.a dynload/libdynload_s.a /testbed/bin/libs/native/linux/x64/org/lwjgl/
RUN mkdir -p bin/libs/native/linux/x64/org/lwjgl \
    && cp /usr/lib/x86_64-linux-gnu/libffi_pic.a bin/libs/native/linux/x64/org/lwjgl/libffi.a \
    && git restore --source="${BASE_COMMIT}" --worktree -- . \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results
CMD ["/bin/bash"]
