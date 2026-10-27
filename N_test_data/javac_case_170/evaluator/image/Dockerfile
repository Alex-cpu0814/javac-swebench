FROM eclipse-temurin:8-jdk-jammy@sha256:185d4ef919b98cd195690c33f3fd93bd49c66c70f0b662e54566c0dbaebea6ce
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git python3 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY context/*.jar /opt/deps/
ADD context/base-source.tar /testbed/
WORKDIR /testbed
RUN git config --global --add safe.directory /testbed && git status --porcelain && java -version && python3 --version
ENV LC_ALL=C.UTF-8
CMD ["/bin/bash"]
