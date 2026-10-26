from __future__ import print_function

import os
import subprocess


def run_child(argv, expected_markers=(), timeout_seconds=60, log_name=None):
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        stdout, stderr = process.communicate()
    out = stdout.decode("utf-8", "replace")
    err = stderr.decode("utf-8", "replace")
    diagnostics = "exit={0}\nstdout:\n{1}\nstderr:\n{2}".format(process.returncode, out, err)
    directory = os.environ.get("BENCHMARK_CHILD_LOG_DIR")
    if directory and log_name:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, log_name + ".log"), "w", encoding="utf-8") as log:
            log.write(diagnostics)
    if timed_out:
        raise AssertionError("Child process timed out after {0}s\n{1}".format(timeout_seconds, diagnostics))
    if process.returncode != 0:
        raise AssertionError("Child JVM failed\n" + diagnostics)
    lines = out.splitlines()
    for marker in expected_markers:
        if lines.count(marker) != 1:
            raise AssertionError("Missing or duplicate completion marker: {0}\n{1}".format(marker, diagnostics))
    return stdout


def jep_pipe(argv):
    return run_child(argv)


def build_java_process_cmd(java_test_name, *args):
    from java.lang import System
    return ["java", "-ea", "-cp", System.getProperty("java.class.path"),
            "-Djava.library.path=" + System.getProperty("java.library.path"),
            "-XX:ErrorFile=/results/hs_err-%p.log", java_test_name] + list(args)
