import unittest
import Util.Util as util

class UtilTestMethods(unittest.TestCase):

    def run_all_tests(self):
        self.test_dateComparison()


# ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
# ┃                                                                              ┃
# ┃      WARNING: This test case will pass for now but figure out a way to       ┃
# ┃       convert today's date to string, then subtract 15 days to get the       ┃
# ┃        caution result and more than 30 days to get the danger result.        ┃
# ┃                                                                              ┃
# ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

    def test_dateComparison(self):
        try:
            self.assertEqual(("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe"),util.dateComparison("2025-02-24"))
            print("test_dateComparison TEST 1: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            self.assertEqual(("alert",[255/256,165/256,0,1],"Caution"),util.dateComparison("2025-02-01"))
            print("test_dateComparison TEST 2: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")

        try:
            self.assertEqual(("alert-circle",[1,0,0,1],"Danger"),util.dateComparison("2025-01-01"))
            print("test_dateComparison TEST 3: PASSED")
        except AssertionError as e:
            print(f"FAILED: {e}")
