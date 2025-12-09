from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_client_data_exception import InvalidClientDataException
from src.exceptions.technician_not_available_exception import TechnicianNotAvailableException
from src.constants.validation_constants import ValidationConstants
from src.constants.financial_constants import FinancialConstants
from src.constants.config_constants import ConfigConstants
class Employee:
    def __init__(self, employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization):
        self._validate_employee_data(employee_id, first_name, last_name, position, salary)
        
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
        self.department = department
        self.address = address
        self.specialization = specialization
        self.is_available = True
        self.assigned_orders = []
        self.performance_rating = 0.0

    def _validate_employee_data(self, employee_id, first_name, last_name, position, salary):
       
        
        if not employee_id:
            raise InvalidClientDataException("employee_id", employee_id)
        if ManualUtils.manual_len(first_name) < ValidationConstants.MIN_CLIENT_NAME_LENGTH:
            raise InvalidClientDataException("first_name", first_name)
        if salary < FinancialConstants.MIN_SALARY:
            raise InvalidClientDataException("salary", salary)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def assign_order(self, repair_order):
        if not self.is_available:
            raise TechnicianNotAvailableException(self.employee_id)
        self.assigned_orders.append(repair_order)
        self.is_available = False

    def complete_order(self, repair_order):
        if self._manual_list_contains(self.assigned_orders, repair_order):
            new_assigned_orders = []
            for order in self.assigned_orders:
                if order != repair_order:
                    new_assigned_orders.append(order)
            self.assigned_orders = new_assigned_orders
            
        if ManualUtils.manual_len(self.assigned_orders) == 0:
            self.is_available = True

    def _manual_list_contains(self, lst, item):
        for element in lst:
            if element == item:
                return True
        return False

    def update_performance_rating(self, new_rating):
       
        
        if ConfigConstants.MIN_EMPLOYEE_RATING <= new_rating <= ConfigConstants.MAX_EMPLOYEE_RATING:
            self.performance_rating = new_rating