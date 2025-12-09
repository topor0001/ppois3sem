from .repair_company_exception import RepairCompanyException

class InvalidPaymentDataException(RepairCompanyException):
    def __init__(self, field_name, field_value):
        message = f"Invalid payment data in field {field_name}: {field_value}"
        super().__init__(message, "INVALID_PAYMENT_DATA")