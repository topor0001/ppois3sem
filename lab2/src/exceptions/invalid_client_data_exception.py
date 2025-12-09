from .repair_company_exception import RepairCompanyException

class InvalidClientDataException(RepairCompanyException):
    def __init__(self, field_name, field_value):
        message = f"Invalid client data in field {field_name}: {field_value}"
        super().__init__(message, "INVALID_CLIENT_DATA")