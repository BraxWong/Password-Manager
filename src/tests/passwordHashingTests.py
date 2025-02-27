import unittest
import Util.passwordHasing as hashing
import bcrypt

class PasswordHashingTestMethods(unittest.TestCase):
    def run_all_tests(self):
        print("\n")
        self.testsRan = 0
        self.testsPassed = 0
        self.testsFailed = 0
        self.test_encodePassword()
        print(f"\n\nTESTS RAN: {self.testsRan}\nTESTS PASSED: {self.testsPassed}\nTESTS FAILED: {self.testsFailed}\n\n")

    def test_encodePassword(self):
        try:
            originalPassword = "12345678910"
            encodedPassword = hashing.encodePassword(originalPassword)
            self.assertIsInstance(encodedPassword, str)
            self.assertNotEqual(encodedPassword, originalPassword)
            self.assertTrue(bcrypt.checkpw(originalPassword.encode('utf-8'), encodedPassword.encode('utf-8')))
            print("test_encodePassword TEST 1: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            originalPassword = "9876543210"
            encodedPassword = hashing.encodePassword(originalPassword)
            self.assertIsInstance(encodedPassword, str)
            self.assertNotEqual(encodedPassword, originalPassword)
            self.assertTrue(bcrypt.checkpw(originalPassword.encode('utf-8'), encodedPassword.encode('utf-8')))
            print("test_encodePassword TEST 2: PASSED")
            self.testsPassed += 1

        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            originalPassword = "ab!d2FGhijkl"
            encodedPassword = hashing.encodePassword(originalPassword)
            self.assertIsInstance(encodedPassword, str)
            self.assertNotEqual(encodedPassword, originalPassword)
            self.assertTrue(bcrypt.checkpw(originalPassword.encode('utf-8'), encodedPassword.encode('utf-8')))
            print("test_encodePassword TEST 3: PASSED")
            self.testsPassed += 1

        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

