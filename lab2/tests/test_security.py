import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.security.user_account import UserAccount
from src.security.security_log import SecurityLog
from src.security.access_control import AccessControl

class TestUserAccount(unittest.TestCase):
    def setUp(self):
        self.user = UserAccount("U001", "testuser", 123456789, "user@test.com", "CLIENT", "2024-01-01", None)

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.is_active)

    def test_password_verification(self):
        result = self.user.verify_password("testpassword")
        self.assertIsInstance(result, bool)

    def test_account_lock_status(self):
        self.assertFalse(self.user.check_account_lock_status())
        
        for _ in range(5):
            self.user.verify_password("wrongpass")
        self.assertTrue(self.user.check_account_lock_status())

    def test_password_strength_validation(self):
        self.assertFalse(self.user.validate_password_strength("weak"))
        self.assertTrue(self.user.validate_password_strength("StrongPass123!"))

    def test_password_reset(self):
        self.user.reset_password("newpassword")
        self.assertEqual(self.user.failed_login_attempts, 0)

    def test_recovery_token_generation(self):
        token = self.user.generate_password_recovery_token()
        self.assertEqual(len(token), 16)

class TestSecurityLog(unittest.TestCase):
    def setUp(self):
        self.user = UserAccount("U001", "testuser", 123456789, "user@test.com", "CLIENT", "2024-01-01", None)
        self.log = SecurityLog("LOG001", self.user, "LOGIN", "2024-01-01", "192.168.1.1", "SUCCESS")

    def test_log_creation(self):
        self.assertEqual(self.log.log_id, "LOG001")
        self.assertEqual(self.log.action, "LOGIN")

    def test_log_event(self):
        self.log.log_security_event("User logged in successfully")
        self.assertEqual(self.log.details, "User logged in successfully")

class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.access_control = AccessControl("ACL001", "ADMIN", "REPORTS", ["READ", "WRITE"], {})

    def test_access_control_creation(self):
        self.assertEqual(self.access_control.control_id, "ACL001")
        self.assertEqual(self.access_control.user_role, "ADMIN")

    def test_permission_check(self):
        user = UserAccount("U001", "admin", 123456, "admin@test.com", "ADMIN", "2024-01-01", None)
        result = self.access_control.check_permission(user, "REPORTS", "READ")
        self.assertTrue(result)

    def test_user_assignment(self):
        user = UserAccount("U001", "admin", 123456, "admin@test.com", "ADMIN", "2024-01-01", None)
        result = self.access_control.assign_to_user(user)
        self.assertTrue(result)
        self.assertIn(user, self.access_control.assigned_users)

if __name__ == '__main__':
    unittest.main()