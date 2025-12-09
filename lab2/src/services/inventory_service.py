from src.utils import manual_utils_instance as ManualUtils

class InventoryManager:
    def __init__(self):
        self.inventory_items = []
        self.suppliers = []
        self.restock_requests = []

    def add_inventory_item(self, part_id, name, description, category, price, quantity, min_stock, supplier, compatibility):
        from src.models.inventory import InventoryItem
        new_item = InventoryItem(part_id, name, description, category, price, quantity, min_stock, supplier, compatibility)
        self.inventory_items.append(new_item)
        return new_item

    def find_item_by_id(self, part_id):
        for item in self.inventory_items:
            if item.part_id == part_id:
                return item
        return None

    def check_part_availability(self, part_id, required_quantity):
        target_item = self.find_item_by_id(part_id)
        if not target_item:
            return False
        return target_item.check_availability(required_quantity)

    def process_restock_requests(self):
        restocked_items = []
        for item in self.inventory_items:
            if item.needs_restocking():
                restock_quantity = item.min_stock_level * 3 - item.quantity_in_stock
                item.restock_items(restock_quantity)
                restocked_items.append({
                    'part_id': item.part_id,
                    'name': item.name,
                    'restocked_quantity': restock_quantity
                })
        return restocked_items

    def calculate_total_inventory_value(self):
        total_value = 0
        for item in self.inventory_items:
            total_value += item.calculate_total_value()
        return total_value