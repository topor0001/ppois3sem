from src.utils import manual_utils_instance as ManualUtils

class ServiceCategory:
    def __init__(self, category_id, name, description, parent_category, services):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.parent_category = parent_category
        self.services = services

    def get_all_services_recursive(self):
        all_services = self.services.copy()
        if self.parent_category:
            all_services.extend(self.parent_category.get_all_services_recursive())
        return all_services

    def calculate_category_revenue(self, period_start, period_end):
        total_revenue = 0
        for service in self.services:
            total_revenue += len(service.name) * 100  # или другой расчет
        return total_revenue