class Salary:
    def __init__(self, salary_id, employee, base_salary, payment_date):
        self.salary_id = salary_id
        self.employee = employee
        self.base_salary = base_salary
        self.payment_date = payment_date
        self.is_paid = False
        self.overtime_pay = 0.0
        self.bonuses = 0.0
        self.deductions = 0.0

    def calculate_total_salary(self):
        return self.base_salary + self.overtime_pay + self.bonuses - self.deductions

    def process_payment(self, company_account, employee_account):
        total = self.calculate_total_salary()
        try:
            company_account.transfer_to_another_account(employee_account, total)
            self.is_paid = True
            return True
        except Exception:
            return False

    def add_overtime(self, hours, rate):
        self.overtime_pay += hours * rate