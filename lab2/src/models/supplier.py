class Supplier:
    def __init__(self, supplier_id, name, contact_person, phone, email, address, rating):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
        self.address = address
        self.rating = rating
        self.delivery_time_days = 7

    def calculate_reliability_score(self):
        return self.rating * 20