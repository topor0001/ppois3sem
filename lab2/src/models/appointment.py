class Appointment:
    def __init__(self, appointment_id, client, technician, scheduled_date, duration_hours, service_type):
        self.appointment_id = appointment_id
        self.client = client
        self.technician = technician
        self.scheduled_date = scheduled_date
        self.duration_hours = duration_hours
        self.service_type = service_type
        self.status = "SCHEDULED"

    def reschedule(self, new_date):
        self.scheduled_date = new_date