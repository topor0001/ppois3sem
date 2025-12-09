from .repair_company_exception import RepairCompanyException

class ServiceNotAvailableException(RepairCompanyException):
    def __init__(self, service_id):
        message = f"Service with ID {service_id} not available"
        super().__init__(message, "SERVICE_NOT_AVAILABLE")