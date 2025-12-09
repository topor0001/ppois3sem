from src.models.employee import Employee

class Manager(Employee):
    def __init__(self, employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization, team_size, budget_responsibility):
        super().__init__(employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization)
        self.team_size = team_size
        self.budget_responsibility = budget_responsibility
        self.managed_employees = []
        self.approved_orders = []

    def approve_repair_order(self, repair_order):
        repair_order.status = "APPROVED"
        self.approved_orders.append(repair_order)
        return True

    def assign_employee_to_department(self, employee, department):
        employee.department = department
        self.managed_employees.append(employee)

    def calculate_team_productivity(self):
        from src.utils import manual_utils_instance as ManualUtils
        
        completed_orders = 0
        for emp in self.managed_employees:
            completed_orders += ManualUtils.manual_len(emp.assigned_orders)
        return completed_orders / self.team_size if self.team_size > 0 else 0