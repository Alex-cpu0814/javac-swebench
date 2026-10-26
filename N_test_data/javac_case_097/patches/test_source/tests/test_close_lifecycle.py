import unittest
from tests.jep_pipe import build_java_process_cmd, run_child


class TestCloseLifecycle(unittest.TestCase):
    def test_same_thread_close(self):
        run_child(build_java_process_cmd("jep.test.TestCloseLifecycle", "same-thread"),
                  ["LIFECYCLE_OK:same-thread"], log_name="same-thread")

    def test_double_close(self):
        run_child(build_java_process_cmd("jep.test.TestCloseLifecycle", "double-close"),
                  ["LIFECYCLE_OK:double-close"], log_name="double-close")
