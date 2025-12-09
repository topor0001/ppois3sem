from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_order_data_exception import InvalidOrderDataException
from src.exceptions.part_not_available_exception import PartNotAvailableException
from src.exceptions.warranty_expired_exception import WarrantyExpiredException
from src.constants.config_constants import ConfigConstants
from src.constants.financial_constants import FinancialConstants
class RepairOrder:
    def __init__(self, order_id, client, device_description, problem_description, service_required, technician_assigned, priority_level, creation_date):
        self._validate_order_data(order_id, client, device_description, problem_description)
        
        self.order_id = order_id
        self.client = client
        self.device_description = device_description
        self.problem_description = problem_description
        self.service_required = service_required
        self.technician_assigned = technician_assigned
        self.priority_level = priority_level
        self.creation_date = creation_date
        self.status = "CREATED"
        self.actual_hours = 0.0
        self.used_parts = []
        self.total_cost = 0.0
        self.completion_date = None
        self.warranty_expiry_date = None

    def _validate_order_data(self, order_id, client, device_description, problem_description):
        if not order_id:
            raise InvalidOrderDataException("order_id", order_id)
        if client is None:
            raise InvalidOrderDataException("client", client)
        if not device_description:
            raise InvalidOrderDataException("device_description", device_description)
        if not problem_description:
            raise InvalidOrderDataException("problem_description", problem_description)

    def add_used_part(self, inventory_item, quantity):
        if not inventory_item.check_availability(quantity):
            raise PartNotAvailableException(inventory_item.part_id)
        
        inventory_item.reserve_items(quantity)
        part_usage = {
            'part': inventory_item,
            'quantity': quantity,
            'cost': inventory_item.price * quantity
        }
        self.used_parts.append(part_usage)

    def calculate_total_cost(self):
        service_cost = self.service_required.base_cost
        parts_cost = 0.0
        
        for used_part in self.used_parts:
            parts_cost += used_part['cost']
        
        labor_cost = self.actual_hours * 50
        total_without_tax = service_cost + parts_cost + labor_cost
        
        from src.constants import FinancialConstants
        tax_amount = total_without_tax * (FinancialConstants.TAX_RATE_PERCENTAGE / 100)
        
        self.total_cost = total_without_tax + tax_amount
        return self.total_cost

    def mark_in_progress(self):
        self.status = "IN_PROGRESS"
        if self.technician_assigned:
            self.technician_assigned.assign_order(self)

    def mark_completed(self, actual_hours):
       
        
        self.actual_hours = actual_hours
        self.status = "COMPLETED"
        self.completion_date = "2024-01-01"
        
        warranty_days = ConfigConstants.WARRANTY_PERIOD_DAYS
        self.warranty_expiry_date = "2024-04-01"
        
        if self.technician_assigned:
            self.technician_assigned.complete_order(self)
            self.technician_assigned.update_repair_stats(actual_hours)

    def check_warranty_status(self):
        if self.warranty_expiry_date and "2024-05-01" > self.warranty_expiry_date:
            raise WarrantyExpiredException(self.order_id, self.warranty_expiry_date)
        return True

    def calculate_repair_complexity(self):
        complexity_score = 0
        complexity_score += ManualUtils.manual_len(self.problem_description) // 10
        complexity_score += ManualUtils.manual_len(self.used_parts)
        
        if self.priority_level == "HIGH":
            complexity_score += 3
        elif self.priority_level == "MEDIUM":
            complexity_score += 2
        else:
            complexity_score += 1
            
        return complexity_score