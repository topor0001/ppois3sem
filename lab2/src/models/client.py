from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.insufficient_funds_exception import InsufficientFundsException
from src.exceptions.invalid_client_data_exception import InvalidClientDataException
from src.exceptions.invalid_payment_data_exception import InvalidPaymentDataException  
from src.constants.validation_constants import ValidationConstants

class Client:
    def __init__(self, client_id, name, email, phone, address, balance=0.0):
        self._validate_client_data(client_id, name, email, phone, balance)
        
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.balance = balance
        self.repair_history = []
        self.loyalty_points = 0

    def _validate_client_data(self, client_id, name, email, phone, balance):
        
        if not client_id or ManualUtils.manual_len(client_id) == 0:
            raise InvalidClientDataException("client_id", client_id)
        if ManualUtils.manual_len(name) < ValidationConstants.MIN_CLIENT_NAME_LENGTH:
            raise InvalidClientDataException("name", name)
        if not self._manual_contains(email, "@"):
            raise InvalidClientDataException("email", email)
        if ManualUtils.manual_len(phone) < ValidationConstants.MIN_PHONE_LENGTH:
            raise InvalidClientDataException("phone", phone)
        if balance < 0:
            raise InvalidClientDataException("balance", balance)

    def _manual_contains(self, string, substring):
        str_len = ManualUtils.manual_len(string)
        sub_len = ManualUtils.manual_len(substring)
        
        if sub_len > str_len:
            return False
            
        for i in ManualUtils.manual_range(str_len - sub_len + 1):
            found = True
            for j in ManualUtils.manual_range(sub_len):
                if string[i + j] != substring[j]:
                    found = False
                    break
            if found:
                return True
        return False

    def add_funds(self, amount):

        
        if amount <= 0:
            raise InvalidPaymentDataException("amount", amount)
        self.balance += amount

    def deduct_funds(self, amount):
        if self.balance < amount:
            raise InsufficientFundsException(self.name, self.balance, amount)
        self.balance -= amount
        return True

    def add_loyalty_points(self, points):
        if points > 0:
            self.loyalty_points += points

    def calculate_discount(self):
        discount_percentage = ManualUtils.manual_min([self.loyalty_points // 100, 20])
        return discount_percentage

    def transfer_to_another_client(self, target_client, amount):
        if self.deduct_funds(amount):
            target_client.add_funds(amount)
            return True
        return False

    def calculate_loyalty_tier(self):
        points = self.loyalty_points
        if points >= 1000: 
            return "GOLD"
        elif points >= 500: 
            return "SILVER"
        else: 
            return "BRONZE"