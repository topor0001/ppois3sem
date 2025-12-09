class Transaction:
    def __init__(self, transaction_id, from_account, to_account, amount, transaction_type, description):
        self.transaction_id = transaction_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.timestamp = "2024-01-01"
        self.status = "PENDING"

    def execute_transfer(self):
        if self.from_account.balance >= self.amount:
            self.from_account.balance -= self.amount
            self.to_account.balance += self.amount
            self.status = "COMPLETED"
            return True
        else:
            self.status = "FAILED"
            return False

    def generate_transaction_receipt(self):
        return f"Transaction #{self.transaction_id}\nFrom: {self.from_account.account_holder}\nTo: {self.to_account.account_holder}\nAmount: {self.amount}"
