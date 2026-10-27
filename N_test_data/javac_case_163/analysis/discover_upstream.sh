#!/usr/bin/env bash
set -euo pipefail
export JAVA_HOME=/opt/jdk
export PATH="$JAVA_HOME/bin:$PATH"
mkdir -p /output/testclasses /output/reports
find /source/junixsocket-common/src/test/java -name '*.java' | sort > /output/sources.txt
javac -encoding UTF-8 -source 8 -target 8 \
  -cp /classes:/deps/junit-platform-console-standalone-1.6.0-M1.jar:/deps/annotations-3.0.1.jar \
  -d /output/testclasses @/output/sources.txt
timeout --kill-after=5s 180s java \
  -cp /classes:/output/testclasses:/deps/junit-platform-console-standalone-1.6.0-M1.jar:/deps/annotations-3.0.1.jar \
  org.junit.platform.console.ConsoleLauncher --scan-class-path --fail-if-no-tests \
  --disable-ansi-colors --reports-dir /output/reports --details tree
