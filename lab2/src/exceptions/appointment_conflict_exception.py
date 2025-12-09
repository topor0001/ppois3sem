from .repair_company_exception import RepairCompanyException

class AppointmentConflictException(RepairCompanyException):
    def __init__(self, technician_id, appointment_date):
        message = f"Appointment conflict for technician {technician_id} on date {appointment_date}"
        super().__init__(message, "APPOINTMENT_CONFLICT")