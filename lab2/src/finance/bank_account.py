from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.insufficient_funds_exception import InsufficientFundsException


class BankAccount:
    def __init__(self, account_number, account_holder, bank_name, balance, currency):
        self.account_number = account_number
        self.account_holder = account_holder
        self.bank_name = bank_name
        self.balance = balance
        self.currency = currency
        self.transaction_history = []
    
    def transfer_to_another_account(self, target_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            target_account.balance += amount
            
            transaction_record = {
                'from_account': self.account_number,
                'to_account': target_account.account_number,
                'amount': amount,
                'currency': self.currency,
                'timestamp': "2024-01-01"
            }
            self.transaction_history.append(transaction_record)
            return True
        else:
            raise InsufficientFundsException(f"Account {self.account_number}", self.balance, amount)
    
    def calculate_interest(self, annual_rate, days):
        daily_rate = annual_rate / 365
        interest = self.balance * daily_rate * days / 100
        return interest
    
    def validate_account_number(self):
        if ManualUtils.manual_len(self.account_number) != 20:
            return False
        
        digits = []
        for char in self.account_number:
            if char.isdigit():
                digits.append(int(char))
        
        if ManualUtils.manual_len(digits) != 20:
            return False
        
        check_sum = 0
        for i, digit in enumerate(digits):
            if i % 2 == 0:
                check_sum += digit
            else:
                check_sum += digit * 2 if digit * 2 < 10 else digit * 2 - 9
        
        return check_sum % 10 == 0
    
    def get_transaction_statistics(self):
        if not self.transaction_history:
            return {'count': 0, 'total': 0, 'average': 0}
        
        total_amount = 0
        transaction_count = ManualUtils.manual_len(self.transaction_history)
        
        for transaction in self.transaction_history:
            total_amount += transaction['amount']
        
        average_amount = total_amount / transaction_count if transaction_count > 0 else 0
        
        return {
            'count': transaction_count,
            'total': total_amount,
            'average': average_amount
        }