from .repair_company_exception import RepairCompanyException

class InvalidOrderDataException(RepairCompanyException):
    def __init__(self, field_name, field_value):
        message = f"Invalid order data in field {field_name}: {field_value}"
        super().__init__(message, "INVALID_ORDER_DATA")