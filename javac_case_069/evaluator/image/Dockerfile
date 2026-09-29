FROM docker.io/library/eclipse-temurin:8-jdk-jammy@sha256:d57e5d0e3e5dd4cabb74feccfdb36249a58c76a3354a33ee8737813df93b7e0d

ARG REPO_URL
ARG BASE_COMMIT
ARG INSTANCE_ID

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/opt/java/openjdk
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update \
    && apt-get install -y --fix-missing --no-install-recommends ant ca-certificates file g++ gcc git libx11-dev make python3 python-is-python3 unzip xz-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

LABEL benchmark.instance_id="${INSTANCE_ID}" benchmark.base_commit="${BASE_COMMIT}" \
      org.opencontainers.image.source="https://github.com/LWJGL/lwjgl3"

RUN git clone --no-checkout "${REPO_URL}" /testbed \
    && cd /testbed \
    && git checkout --detach "${BASE_COMMIT}" \
    && git remote remove origin \
    && git config core.autocrlf false \
    && git for-each-ref --format='delete %(refname)' refs/heads refs/remotes refs/tags | git update-ref --stdin \
    && git reflog expire --expire=now --all \
    && git gc --prune=now \
    && test "$(git rev-parse HEAD)" = "${BASE_COMMIT}" \
    && test -z "$(git status --porcelain)" \
    && mkdir -p /benchmark /inputs /results

# The historical Ant build points at the retired central.maven.org hostname.
# Resolve dependencies and compile the unmodified Base while the image build
# still has network access; evaluation itself runs with --network none.
RUN cd /testbed \
    && sed -i 's#http://central.maven.org/maven2#https://repo1.maven.org/maven2#g' config/build-definitions.xml \
    && C_INCLUDE_PATH=/testbed/modules/lwjgl/core/src/main/c/dyncall ant -Dbuild.type=release/3.2.1 -Dbuild.offline=false \
        -Dbinding.assimp=false -Dbinding.bgfx=false -Dbinding.egl=false \
        -Dbinding.glfw=false -Dbinding.jawt=false -Dbinding.jemalloc=false \
        -Dbinding.lmdb=false -Dbinding.lz4=false -Dbinding.nanovg=false \
        -Dbinding.nfd=false -Dbinding.nuklear=false -Dbinding.odbc=false \
        -Dbinding.openal=false -Dbinding.opencl=false -Dbinding.opengl=false \
        -Dbinding.opengles=false -Dbinding.openvr=false -Dbinding.par=false \
        -Dbinding.remotery=false -Dbinding.rpmalloc=false -Dbinding.sse=false \
        -Dbinding.stb=false -Dbinding.tinyexr=false -Dbinding.tinyfd=false \
        -Dbinding.tootle=false -Dbinding.vma=false -Dbinding.vulkan=false \
        -Dbinding.xxhash=false -Dbinding.yoga=false -Dbinding.zstd=false \
        compile-templates compile-native \
    && mkdir -p bin/classes/test \
    && javac -cp "bin/classes/lwjgl/core:bin/libs/java/jsr305.jar:bin/libs/java/testng.jar" \
        -d bin/classes/test \
        modules/lwjgl/core/src/test/java/org/lwjgl/system/MemoryUtilTest.java \
    && git checkout -- modules/lwjgl/core/src/generated \
    && git checkout -- config/build-definitions.xml

WORKDIR /testbed
CMD ["/bin/bash"]
