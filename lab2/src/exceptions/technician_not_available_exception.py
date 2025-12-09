from .repair_company_exception import RepairCompanyException

class TechnicianNotAvailableException(RepairCompanyException):
    def __init__(self, technician_id):
        message = f"Technician with ID {technician_id} not available"
        super().__init__(message, "TECHNICIAN_NOT_AVAILABLE")