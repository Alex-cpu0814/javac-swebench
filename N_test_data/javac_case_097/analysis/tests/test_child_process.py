"""Check success markers, failure diagnostics, and bounded child execution."""
import importlib.util
from pathlib import Path
import sys
import unittest

path = Path(__file__).resolve().parents[2] / "patches/test_source/tests/jep_pipe.py"
spec = importlib.util.spec_from_file_location("case097_pipe", path)
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)


class ChildProcessTest(unittest.TestCase):
    def test_success_requires_marker(self):
        result = pipe.run_child([sys.executable, "-c", "print('DONE')"], ["DONE"])
        self.assertEqual(result.strip(), b"DONE")

    def test_zero_exit_without_completion_fails(self):
        with self.assertRaisesRegex(AssertionError, "Missing or duplicate completion marker"):
            pipe.run_child([sys.executable, "-c", "pass"], ["DONE"])

    def test_duplicate_marker_fails(self):
        with self.assertRaisesRegex(AssertionError, "Missing or duplicate completion marker"):
            pipe.run_child([sys.executable, "-c", "print('DONE'); print('DONE')"], ["DONE"])

    def test_nonzero_exit_retains_output(self):
        with self.assertRaisesRegex(AssertionError, "(?s)Child JVM failed.*stdout:.*OUT.*stderr:.*ERR"):
            pipe.run_child([sys.executable, "-c", "import sys; print('OUT'); print('ERR', file=sys.stderr); sys.exit(1)"])

    def test_timeout_fails_and_reaps_child(self):
        with self.assertRaisesRegex(AssertionError, "timed out"):
            pipe.run_child([sys.executable, "-c", "import time; time.sleep(5)"], timeout_seconds=0.1)


if __name__ == "__main__":
    unittest.main()
