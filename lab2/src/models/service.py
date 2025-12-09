from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.service_not_available_exception import ServiceNotAvailableException
from src.constants.config_constants import ConfigConstants
from src.constants.financial_constants import FinancialConstants

class RepairService:
    def __init__(self, service_id, name, description, base_cost, estimated_hours, required_parts, skill_level_required, warranty_period):
        self._validate_service_data(service_id, name, base_cost, estimated_hours)
        
        self.service_id = service_id
        self.name = name
        self.description = description
        self.base_cost = base_cost
        self.estimated_hours = estimated_hours
        self.required_parts = required_parts
        self.skill_level_required = skill_level_required
        self.warranty_period = warranty_period
        self.is_available = True

    def _validate_service_data(self, service_id, name, base_cost, estimated_hours):
       
        
        if not service_id:
            raise ServiceNotAvailableException(service_id)
        if not name:
            raise ServiceNotAvailableException(service_id)
        if base_cost < ConfigConstants.MIN_SERVICE_COST:
            raise ServiceNotAvailableException(service_id)
        if estimated_hours < ConfigConstants.MIN_REPAIR_HOURS:
            raise ServiceNotAvailableException(service_id)

    def calculate_final_cost(self, complexity_multiplier, urgency_multiplier):
        base_total = self.base_cost * complexity_multiplier
        if urgency_multiplier > 1:
            base_total *= urgency_multiplier
        return base_total

    def check_technician_qualification(self, technician_skill_level):
        return technician_skill_level >= self.skill_level_required

    def get_required_parts_list(self):
        return self.required_parts.copy()