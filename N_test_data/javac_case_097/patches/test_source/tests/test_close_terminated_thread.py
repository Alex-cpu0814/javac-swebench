import unittest
from tests.jep_pipe import build_java_process_cmd, run_child


class TestCloseTerminatedThread(unittest.TestCase):
    def test_close_terminated_thread(self):
        run_child(build_java_process_cmd("jep.test.TestCloseTerminatedThread"),
                  ["CLOSE_STEP:0", "CLOSE_STEP:1", "CLOSE_STEP:2", "CLOSE_OK"],
                  log_name="terminated-thread")
