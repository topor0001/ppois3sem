from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_part_data_exception import InvalidPartDataException
from src.exceptions.part_not_available_exception import PartNotAvailableException
from src.constants.config_constants import ConfigConstants
from src.constants.financial_constants import FinancialConstants
class InventoryItem:
    def __init__(self, part_id, name, description, category, price, quantity_in_stock, min_stock_level, supplier_info, compatibility_list):
        self._validate_inventory_data(part_id, name, price, quantity_in_stock)
        
        self.part_id = part_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.min_stock_level = min_stock_level
        self.supplier_info = supplier_info
        self.compatibility_list = compatibility_list

    def _validate_inventory_data(self, part_id, name, price, quantity_in_stock):
       
        
        if not part_id:
            raise InvalidPartDataException("part_id", part_id)
        if not name:
            raise InvalidPartDataException("name", name)
        if price <= 0:
            raise InvalidPartDataException("price", price)
        if quantity_in_stock < 0:
            raise InvalidPartDataException("quantity_in_stock", quantity_in_stock)

    def check_availability(self, required_quantity):
        return self.quantity_in_stock >= required_quantity

    def reserve_items(self, quantity):
        if not self.check_availability(quantity):
            raise PartNotAvailableException(self.part_id)
        self.quantity_in_stock -= quantity

    def restock_items(self, quantity):
        if quantity > 0:
            self.quantity_in_stock += quantity

    def needs_restocking(self):
        return self.quantity_in_stock <= self.min_stock_level

    def calculate_total_value(self):
        return self.price * self.quantity_in_stock