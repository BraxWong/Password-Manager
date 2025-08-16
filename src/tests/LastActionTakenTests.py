import unittest
import LastActionTaken
from datetime import datetime, timedelta
import time

class LastActionTakenTestMethods(unittest.TestCase):
    def run_all_tests(self):
        print("\n")
        self.testsRan = 0
        self.testsPassed = 0
        self.testsFailed = 0
        testStartTime = time.perf_counter()
        self.test_check_login_required()
        testEndTime = time.perf_counter()
        print(f"\n\nTESTS RAN: {self.testsRan}\nTESTS PASSED: {self.testsPassed}\nTESTS FAILED: {self.testsFailed}\nTESTS RUNTIME: {testEndTime-testStartTime:0.6f} seconds\n\n")

    def test_check_login_required(self):
        try:
            self.last_action_taken = LastActionTaken.last_action_taken()
            self.now = datetime.now()
            self.last_action_taken.last_action = self.now - timedelta(minutes=20) 
            self.assertIsInstance(self.last_action_taken.last_action, datetime)
            self.assertTrue(self.last_action_taken.check_login_required())
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed +=1
        self.testsRan += 1

        try:
            self.last_action_taken = LastActionTaken.last_action_taken()
            self.now = datetime.now()
            self.last_action_taken.last_action = self.now - timedelta(minutes=5) 
            self.assertIsInstance(self.last_action_taken.last_action, datetime)
            self.assertFalse(self.last_action_taken.check_login_required())
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed +=1
        self.testsRan += 1
