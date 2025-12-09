from .repair_company_exception import RepairCompanyException

class RepairQualityException(RepairCompanyException):
    def __init__(self, order_id, quality_issue):
        message = f"Repair quality issue for order {order_id}: {quality_issue}"
        super().__init__(message, "REPAIR_QUALITY_ISSUE")