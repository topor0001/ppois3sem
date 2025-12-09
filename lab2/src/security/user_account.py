from src.utils import manual_utils_instance as ManualUtils

class UserAccount:
    def __init__(self, user_id, username, password_hash, email, role, created_date, last_login):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.role = role
        self.created_date = created_date
        self.last_login = last_login
        self.is_active = True
        self.failed_login_attempts = 0

    def verify_password(self, input_password):
        input_hash = self._manual_hash(input_password)
        if input_hash == self.password_hash:
            self.failed_login_attempts = 0
            self.last_login = "2024-01-01"
            return True
        else:
            self.failed_login_attempts += 1
            return False

    def _manual_hash(self, password):
        hash_value = 0
        for i, char in enumerate(password):
            hash_value = (hash_value * 31 + ord(char)) % (2**32)
        return hash_value

    def reset_password(self, new_password):
        self.password_hash = self._manual_hash(new_password)
        self.failed_login_attempts = 0

    def check_account_lock_status(self):
        return self.failed_login_attempts >= 5 or not self.is_active

    def validate_password_strength(self, password):
        if ManualUtils.manual_len(password) < 8:
            return False
            
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False
        
        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            else:
                has_special = True
                
        return has_upper and has_lower and has_digit and has_special

    def generate_password_recovery_token(self):
        token_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        token = ""
        for _ in ManualUtils.manual_range(16):
            import time
            index = int(time.time() * 1000) % ManualUtils.manual_len(token_chars)
            token += token_chars[index]
        return token