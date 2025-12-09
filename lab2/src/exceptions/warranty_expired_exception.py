from .repair_company_exception import RepairCompanyException

class WarrantyExpiredException(RepairCompanyException):
    def __init__(self, order_id, expiry_date):
        message = f"Warranty for order {order_id} expired on {expiry_date}"
        super().__init__(message, "WARRANTY_EXPIRED")