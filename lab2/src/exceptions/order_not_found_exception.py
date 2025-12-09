
from .repair_company_exception import RepairCompanyException

class OrderNotFoundException(RepairCompanyException):
    def __init__(self, order_id):
        message = f"Order with ID {order_id} not found"
        super().__init__(message, "ORDER_NOT_FOUND")
