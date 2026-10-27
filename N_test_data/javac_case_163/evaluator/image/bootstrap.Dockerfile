FROM ubuntu:16.04@sha256:1f1a2d56de1d604801a9671f301190704c25d604a416f59e03c04f5c6ffee0d6
RUN apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install -y --no-install-recommends clang gcc libc6-dev binutils \
       ca-certificates xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
