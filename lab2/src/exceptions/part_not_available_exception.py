from .repair_company_exception import RepairCompanyException

class PartNotAvailableException(RepairCompanyException):
    def __init__(self, part_id):
        message = f"Part with ID {part_id} not available"
        super().__init__(message, "PART_NOT_AVAILABLE")