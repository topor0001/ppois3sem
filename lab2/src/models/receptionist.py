from src.models.employee import Employee

class Receptionist(Employee):
    def __init__(self, employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization, shift_schedule, languages):
        super().__init__(employee_id, first_name, last_name, position, salary, hire_date, department, address, specialization)
        self.shift_schedule = shift_schedule
        self.languages = languages
        self.processed_appointments = []

    def handle_phone_inquiry(self, caller, inquiry_type):
        return f"Handled phone inquiry from {caller} about: {inquiry_type}"

    def generate_daily_schedule(self, date):
        from src.utils import manual_utils_instance as ManualUtils
        
        daily_appointments = []
        for app in self.processed_appointments:
            if app.scheduled_date == date:
                daily_appointments.append(app)
                
        return f"Schedule for {date}: {ManualUtils.manual_len(daily_appointments)} appointments"