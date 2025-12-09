from .repair_company_exception import RepairCompanyException

class InvalidPartDataException(RepairCompanyException):
    def __init__(self, field_name, field_value):
        message = f"Invalid part data in field {field_name}: {field_value}"
        super().__init__(message, "INVALID_PART_DATA")