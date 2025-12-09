from .repair_company_exception import RepairCompanyException

class InsufficientFundsException(RepairCompanyException):
    def __init__(self, client_name, current_balance, required_amount):
        message = f"Insufficient funds for client {client_name}. Current: {current_balance}, Required: {required_amount}"
        super().__init__(message, "INSUFFICIENT_FUNDS")