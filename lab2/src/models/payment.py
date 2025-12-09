from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_payment_data_exception import InvalidPaymentDataException
from src.exceptions.insufficient_funds_exception import InsufficientFundsException
from src.constants.financial_constants import FinancialConstants

class Payment:
    def __init__(self, payment_id, client, repair_order, amount, payment_method, payment_date):
        self._validate_payment_data(payment_id, client, amount)
        
        self.payment_id = payment_id
        self.client = client
        self.repair_order = repair_order
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.is_processed = False
        self.transaction_id = None

    def _validate_payment_data(self, payment_id, client, amount):
        
        if not payment_id:
            raise InvalidPaymentDataException("payment_id", payment_id)
        if client is None:
            raise InvalidPaymentDataException("client", client)
        if amount < FinancialConstants.MIN_PAYMENT_AMOUNT:
            raise InvalidPaymentDataException("amount", amount)

    def process_payment(self):
        try:
            self.client.deduct_funds(self.amount)
            self.is_processed = True
            self.transaction_id = self._generate_transaction_id()
            return True
        except InsufficientFundsException as error:
            raise error

    def _generate_transaction_id(self):
        base_id = f"TXN{self.payment_id}"
        date_part = self.payment_date.replace("-", "")
        return base_id + date_part

    def generate_receipt(self):
        if not self.is_processed:
            return "Payment not processed"
        
        receipt_lines = []
        receipt_lines.append("PAYMENT RECEIPT")
        receipt_lines.append(f"Payment ID: {self.payment_id}")
        receipt_lines.append(f"Client: {self.client.name}")
        receipt_lines.append(f"Amount: ${self.amount:.2f}")
        receipt_lines.append(f"Method: {self.payment_method}")
        receipt_lines.append(f"Date: {self.payment_date}")
        receipt_lines.append(f"Transaction ID: {self.transaction_id}")
        
        return ManualUtils.manual_join(receipt_lines, "\n")

    def process_installment_plan(self, num_installments):
        if num_installments <= 0:
            return []
            
        installment_amount = self.amount / num_installments
        installments = []
        for _ in ManualUtils.manual_range(num_installments):
            installments.append(installment_amount)
        return installments

    def validate_payment_method(self):
        valid_methods = ["CASH", "CARD", "BANK_TRANSFER", "DIGITAL_WALLET"]
        return self._manual_list_contains(valid_methods, self.payment_method)

    def _manual_list_contains(self, lst, item):
        for element in lst:
            if element == item:
                return True
        return False