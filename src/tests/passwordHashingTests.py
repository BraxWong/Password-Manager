import unittest
import Util.passwordHasing as hashing
import bcrypt
import time

class PasswordHashingTestMethods(unittest.TestCase):
    def run_all_tests(self):
        print("\n")
        self.testsRan = 0
        self.testsPassed = 0
        self.testsFailed = 0
        testStartTime = time.perf_counter()
        self.test_encodePassword()
        self.test_checkPassword()
        testEndTime = time.perf_counter()
        print(f"\n\nTESTS RAN: {self.testsRan}\nTESTS PASSED: {self.testsPassed}\nTESTS FAILED: {self.testsFailed}\nTESTS RUNTIME: {testEndTime-testStartTime:0.4f} seconds\n\n")

    def test_encodePassword(self):
        try:
            originalPassword = "12345678910"
            encodedPassword = hashing.encode_password(originalPassword)
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
            encodedPassword = hashing.encode_password(originalPassword)
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
            encodedPassword = hashing.encode_password(originalPassword)
            self.assertIsInstance(encodedPassword, str)
            self.assertNotEqual(encodedPassword, originalPassword)
            self.assertTrue(bcrypt.checkpw(originalPassword.encode('utf-8'), encodedPassword.encode('utf-8')))
            print("test_encodePassword TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

    def test_checkPassword(self):
        try:
            originalPassword = "12345678"
            hashedPassword = hashing.encode_password(originalPassword)
            self.assertTrue(hashing.check_password(originalPassword,hashedPassword))
            print("test_checkPassword TEST 1: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            originalPassword = "ab2Soi20Xn2"
            hashedPassword = hashing.encode_password(originalPassword)
            self.assertTrue(hashing.check_password(originalPassword,hashedPassword))
            print("test_checkPassword TEST 2: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1

        try:
            originalPassword = "Skj93XN921x"
            hashedPassword = hashing.encode_password(originalPassword)
            self.assertTrue(hashing.check_password(originalPassword,hashedPassword))
            print("test_checkPassword TEST 3: PASSED")
            self.testsPassed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            self.testsFailed += 1
        self.testsRan+=1