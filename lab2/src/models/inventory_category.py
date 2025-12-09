from src.utils import manual_utils_instance as ManualUtils

class InventoryCategory:
    def __init__(self, category_id, name, description, parent_category, items):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.parent_category = parent_category
        self.items = items

    def get_total_category_value(self):
        total_value = 0
        for item in self.items:
            total_value += item.calculate_total_value()
        return total_value

    def get_low_stock_items(self):
        low_stock_items = []
        for item in self.items:
            if item.needs_restocking():
                low_stock_items.append(item)
        return low_stock_items