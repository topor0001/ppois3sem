from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.order_not_found_exception import OrderNotFoundException
from src.exceptions.technician_not_available_exception import TechnicianNotAvailableException

class RepairServiceManager:
    def __init__(self):
        self.active_orders = []
        self.completed_orders = []
        self.available_technicians = []
        self.repair_services = []

    def _find_order_by_id(self, order_id):
        for order in self.active_orders:
            if order.order_id == order_id:
                return order
        for order in self.completed_orders:
            if order.order_id == order_id:
                return order
        return None

    def assign_technician_to_order(self, order_id, technician):
        target_order = self._find_order_by_id(order_id)
        if not target_order:
            raise OrderNotFoundException(order_id)
        
        if not self._manual_list_contains(self.available_technicians, technician):
            raise TechnicianNotAvailableException(technician.employee_id)
        
        target_order.technician_assigned = technician
        target_order.mark_in_progress()

    def _manual_list_contains(self, lst, item):
        for element in lst:
            if element == item:
                return True
        return False

    def complete_repair_order(self, order_id, actual_hours, used_parts):
        target_order = self._find_order_by_id(order_id)
        if not target_order:
            raise OrderNotFoundException(order_id)
        
        for part_data in used_parts:
            target_order.add_used_part(part_data['part'], part_data['quantity'])
        
        target_order.mark_completed(actual_hours)
        
        new_active_orders = []
        for order in self.active_orders:
            if order.order_id != order_id:
                new_active_orders.append(order)
        self.active_orders = new_active_orders
        
        self.completed_orders.append(target_order)
        
        return target_order.calculate_total_cost()

    def calculate_technician_workload(self, technician_id):
        workload_count = 0
        for order in self.active_orders:
            if order.technician_assigned and order.technician_assigned.employee_id == technician_id:
                workload_count += 1
        return workload_count

    def find_available_technician(self, required_skill_level):
        available_techs = []
        for tech in self.available_technicians:
            if tech.skill_level >= required_skill_level:
                available_techs.append(tech)
                
        if available_techs:
            best_tech = available_techs[0]
            for tech in available_techs:
                if tech.skill_level > best_tech.skill_level:
                    best_tech = tech
            return best_tech
        return None