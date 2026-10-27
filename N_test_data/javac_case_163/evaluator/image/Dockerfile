FROM centos@sha256:a93df2e96e07f56ea48f215425c6f1673ab922927894595bb5c0ee4c5a955133 AS legacy
FROM local/case163-junixsocket:builder
ARG BASE_COMMIT=90716d6008c5c9cfa8a061f3d23531acaea29777
ARG INSTANCE_ID=kohlschutter__junixsocket-81
RUN apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install -y --no-install-recommends git python3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=legacy / /opt/legacy/
ADD context/OpenJDK8U-jdk_x64_linux_hotspot_8u292b10.tar.gz /opt/java/
COPY context/qemu-x86_64-static /opt/tools/qemu-x86_64-static
COPY context/junit-platform-console-standalone-1.6.0-M1.jar /opt/deps/junit-console.jar
COPY context/annotations-3.0.1.jar /opt/deps/annotations.jar
ADD context/base-source.tar /testbed/
ENV JAVA_HOME=/opt/java/jdk8u292-b10
ENV PATH=${JAVA_HOME}/bin:${PATH}
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN chmod 0755 /opt/tools/qemu-x86_64-static \
    && ln -s /usr/bin/python3 /usr/local/bin/python \
    && mkdir -p /benchmark /inputs /results \
    && git -C /testbed config core.autocrlf false \
    && test "$(git -C /testbed rev-parse HEAD)" = "$BASE_COMMIT" \
    && test -z "$(git -C /testbed status --porcelain)" \
    && /opt/tools/qemu-x86_64-static -L /opt/legacy /opt/legacy/lib64/libc.so.6 \
    && /opt/tools/qemu-x86_64-static -L /opt/legacy ${JAVA_HOME}/bin/java \
       -Xint -Xmx64m -XX:+UseSerialGC -XX:ActiveProcessorCount=2 -version
LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}"
WORKDIR /testbed
CMD ["/bin/bash"]
