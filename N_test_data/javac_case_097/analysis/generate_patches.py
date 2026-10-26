"""Generate exact upstream gold, protected tests and overbroad-fix controls."""
import argparse
import difflib
from pathlib import Path
import subprocess

CASE = Path(__file__).resolve().parents[1]
BASE = "e4f13ea277ce4809688dde766cc9fd173ec6f63d"
FIX = "767509de81f3a11b1ca54e23619d3226944a141e"


def diff(path, before, after):
    header = "diff --git a/{0} b/{0}\n".format(path)
    if before is None:
        header += "new file mode 100644\n"
    lines = difflib.unified_diff((before or "").splitlines(keepends=True), after.splitlines(keepends=True),
                                fromfile="a/" + path if before is not None else "/dev/null", tofile="b/" + path)
    return header + "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-dir", type=Path, required=True)
    args = parser.parse_args()
    git = ["git", "--git-dir=" + str(args.git_dir)]
    def source(commit, path):
        return subprocess.check_output(git + ["show", commit + ":" + path]).decode("utf-8")
    gold = subprocess.check_output(git + ["diff", BASE, FIX, "--"])
    (CASE / "patches/gold_patch.diff").write_bytes(gold)
    init = source(BASE, "tests/__init__.py")
    (CASE / "patches/test_source/tests/__init__.py").write_text(
        init + "\nfrom .test_close_terminated_thread import *\nfrom .test_close_lifecycle import *\n", encoding="utf-8", newline="\n")
    chunks = []
    for file in sorted((CASE / "patches/test_source").rglob("*")):
        if not file.is_file() or "__pycache__" in file.parts:
            continue
        path = file.relative_to(CASE / "patches/test_source").as_posix()
        exists = subprocess.run(git + ["cat-file", "-e", BASE + ":" + path], capture_output=True).returncode == 0
        chunks.append(diff(path, source(BASE, path) if exists else None, file.read_text(encoding="utf-8")))
    (CASE / "patches/test_patch.diff").write_text("".join(chunks), encoding="utf-8", newline="\n")
    changed = subprocess.check_output(git + ["diff", "--name-only", BASE, FIX], text=True).splitlines()
    jep = source(FIX, "src/jep/Jep.java")
    start = jep.index("    public synchronized void close() {")
    end = jep.index("    private native void close(long tstate);", start)
    for name, body in (("close_noop", "    public synchronized void close() {\n    }\n\n"),
                       ("close_flag_only", "    public synchronized void close() {\n        this.closed = true;\n        this.tstate = 0;\n        threadUsed.set(false);\n    }\n\n")):
        altered = jep[:start] + body + jep[end:]
        control = "".join(diff(path, source(BASE, path), altered if path == "src/jep/Jep.java" else source(FIX, path))
                          for path in changed)
        (CASE / "verification/controls" / (name + ".patch")).write_text(control, encoding="utf-8", newline="\n")
    (CASE / "verification/controls/test_tamper.patch").write_text(diff(
        "src/jep/test/TestCloseTerminatedThread.java", None,
        "package jep.test;\npublic class TestCloseTerminatedThread {}\n"), encoding="utf-8", newline="\n")
    print("Generated full upstream gold ({} files), protected tests, and controls".format(len(changed)))


if __name__ == "__main__":
    main()
