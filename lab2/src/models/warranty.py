from src.exceptions import WarrantyExpiredException

class Warranty:
    def __init__(self, warranty_id, repair_order, duration_days, start_date, terms_conditions):
        self.warranty_id = warranty_id
        self.repair_order = repair_order
        self.duration_days = duration_days
        self.start_date = start_date
        self.terms_conditions = terms_conditions
        self.claims_count = 0

    def is_valid(self):
        return self.claims_count < 3

    def register_claim(self):
        self.claims_count += 1