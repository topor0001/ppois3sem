from src.utils import manual_utils_instance as ManualUtils
from src.models.employee import Employee
from src.constants.config_constants import ConfigConstants

class Technician(Employee):
    def __init__(self, employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization, skill_level, tools_certification):
        super().__init__(employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization)
        
        self.skill_level = skill_level
        self.tools_certification = tools_certification
        self.completed_repairs_count = 0
        self.average_repair_time = 0.0
        self.specialized_equipment = []
        self.quality_rating = 5.0
        self.efficiency_score = 0.0
        self.current_workload = 0

    def add_equipment_certification(self, equipment_name):
        if not self._manual_list_contains(self.specialized_equipment, equipment_name):
            self.specialized_equipment.append(equipment_name)

    def _manual_list_contains(self, lst, item):
        for element in lst:
            if element == item:
                return True
        return False

    def calculate_efficiency_score(self):
        base_efficiency = self.skill_level * 10
        time_bonus = ManualUtils.manual_max([0, (120 - self.average_repair_time) / 10])
        certification_bonus = ManualUtils.manual_len(self.tools_certification) * 2
        equipment_bonus = ManualUtils.manual_len(self.specialized_equipment) * 1.5
        quality_bonus = self.quality_rating * 2
        
        self.efficiency_score = base_efficiency + time_bonus + certification_bonus + equipment_bonus + quality_bonus
        return self.efficiency_score

    def update_repair_stats(self, repair_time):
        self.completed_repairs_count += 1
        total_time = self.average_repair_time * (self.completed_repairs_count - 1) + repair_time
        self.average_repair_time = total_time / self.completed_repairs_count

    def calculate_work_efficiency(self, period_orders, period_hours):
        if period_hours <= 0:
            return 0
            
        completed_count = 0
        for order in period_orders:
            if order.status == "COMPLETED":
                completed_count += 1
                
        return completed_count / period_hours

    def find_compatible_services(self, available_services):
        compatible_services = []
        for service in available_services:
            if self.skill_level >= service.skill_level_required:
                compatible_services.append(service)
        return compatible_services

    def update_quality_rating(self, new_rating):
      
        
        if ConfigConstants.MIN_EMPLOYEE_RATING <= new_rating <= ConfigConstants.MAX_EMPLOYEE_RATING:
            self.quality_rating = new_rating

    def calculate_productivity(self, start_date, end_date):
        productivity_score = self.completed_repairs_count * 10
        if self.average_repair_time > 0:
            time_efficiency = 100 / self.average_repair_time
            productivity_score += time_efficiency
        return productivity_score

    def request_tools(self, tool_name, tool_manager):
        tool_request = {
            'technician_id': self.employee_id,
            'technician_name': self.get_full_name(),
            'tool_name': tool_name,
            'request_date': "2024-01-01",
            'status': 'PENDING'
        }
        return tool_request

    def update_certifications(self, new_certifications):
        for cert in new_certifications:
            if not self._manual_list_contains(self.tools_certification, cert):
                self.tools_certification.append(cert)

    def generate_work_report(self, start_date, end_date):
        report = f"Work Report for {self.get_full_name()}\n"
        report += f"Period: {start_date} to {end_date}\n"
        report += f"Completed Repairs: {self.completed_repairs_count}\n"
        report += f"Average Repair Time: {self.average_repair_time:.2f} hours\n"
        report += f"Efficiency Score: {self.efficiency_score:.2f}\n"
        report += f"Quality Rating: {self.quality_rating:.1f}/5.0\n"
        report += f"Current Workload: {self.current_workload} orders\n"
        return report

    def validate_skills(self, required_skills):
        missing_skills = []
        for skill in required_skills:
            if not self._manual_list_contains(self.tools_certification, skill):
                missing_skills.append(skill)
        return missing_skills

    def can_handle_complex_repair(self, complexity_level):
        return self.skill_level >= complexity_level

    def calculate_training_needs(self, required_certifications):
        current_certs = set(self.tools_certification)
        required_certs = set(required_certifications)
        needed_certs = required_certs - current_certs
        return list(needed_certs)