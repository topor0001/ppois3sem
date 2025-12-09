from src.utils import manual_utils_instance as ManualUtils

class ServicePackage:
    def __init__(self, package_id, name, description, included_services, discount_rate, validity_period):
        self.package_id = package_id
        self.name = name
        self.description = description
        self.included_services = included_services
        self.discount_rate = discount_rate
        self.validity_period = validity_period
        self.active_clients = []

    def calculate_package_price(self):
        base_price = 0
        for service in self.included_services:
            base_price += service.base_cost
        return base_price * (1 - self.discount_rate / 100)

    def add_client_to_package(self, client):
        if not self._manual_list_contains(self.active_clients, client):
            self.active_clients.append(client)
            return True
        return False

    def _manual_list_contains(self, lst, item):
        for element in lst:
            if element == item:
                return True
        return False