import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.repair_service import RepairServiceManager
from src.services.inventory_service import InventoryManager
from src.services.quality_control import QualityControlManager
from src.models.client import Client
from src.models.address import Address
from src.models.technician import Technician
from src.models.service import RepairService
from src.models.repair_order import RepairOrder
from src.models.inventory import InventoryItem
from src.exceptions import OrderNotFoundException, TechnicianNotAvailableException
from src.exceptions.order_not_found_exception import OrderNotFoundException
from src.exceptions.technician_not_available_exception import TechnicianNotAvailableException
class TestRepairServiceManager(unittest.TestCase):
    def setUp(self):
        self.manager = RepairServiceManager()
        self.address = Address("Test St", "City", "ST", "12345", "Country", "123")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.technician = Technician("T001", "Tech", "Nician", "Technician", 50000.0,
                                   "2023-01-01", "Repair", self.address, "Electronics", 7, [])
        self.service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)

    def test_find_order_by_id(self):
        order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")
        self.manager.active_orders.append(order)
        
        found = self.manager._find_order_by_id("RO001")
        self.assertEqual(found, order)
        
        not_found = self.manager._find_order_by_id("NONEXISTENT")
        self.assertIsNone(not_found)

    def test_assign_technician(self):
        order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")
        self.manager.active_orders.append(order)
        self.manager.available_technicians.append(self.technician)
        
        self.manager.assign_technician_to_order("RO001", self.technician)
        self.assertEqual(order.technician_assigned, self.technician)
        self.assertEqual(order.status, "IN_PROGRESS")

    def test_complete_repair_order(self):
        order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, self.technician, "NORMAL", "2024-01-01")
        self.manager.active_orders.append(order)
        
        part = InventoryItem("P001", "Part", "Description", "Category", 50.0, 10, 2, "Supplier", [])
        used_parts = [{'part': part, 'quantity': 1}]
        
        total_cost = self.manager.complete_repair_order("RO001", 2.0, used_parts)
        self.assertGreater(total_cost, 0)
        self.assertEqual(order.status, "COMPLETED")
        self.assertIn(order, self.manager.completed_orders)
        self.assertNotIn(order, self.manager.active_orders)

    def test_technician_workload(self):
        order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, self.technician, "NORMAL", "2024-01-01")
        self.manager.active_orders.append(order)
        
        workload = self.manager.calculate_technician_workload("T001")
        self.assertEqual(workload, 1)

    def test_find_available_technician(self):
        self.manager.available_technicians.append(self.technician)
        
        found = self.manager.find_available_technician(5)
        self.assertEqual(found, self.technician)
        
        not_found = self.manager.find_available_technician(9)
        self.assertIsNone(not_found)

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = InventoryManager()
        self.item = InventoryItem("P001", "Test Part", "Description", "Category", 25.0, 10, 2, "Supplier", [])

    def test_add_inventory_item(self):
        new_item = self.manager.add_inventory_item("P002", "New Part", "Desc", "Cat", 30.0, 15, 3, "Sup", [])
        self.assertEqual(new_item.part_id, "P002")
        self.assertIn(new_item, self.manager.inventory_items)

    def test_find_item_by_id(self):
        self.manager.inventory_items.append(self.item)
        
        found = self.manager.find_item_by_id("P001")
        self.assertEqual(found, self.item)
        
        not_found = self.manager.find_item_by_id("P999")
        self.assertIsNone(not_found)

    def test_check_part_availability(self):
        self.manager.inventory_items.append(self.item)
        
        self.assertTrue(self.manager.check_part_availability("P001", 5))
        self.assertFalse(self.manager.check_part_availability("P001", 15))

    def test_process_restock_requests(self):
        low_stock_item = InventoryItem("P002", "Low Stock", "Desc", "Cat", 10.0, 1, 5, "Sup", [])
        self.manager.inventory_items.append(low_stock_item)
        
        restocked = self.manager.process_restock_requests()
        self.assertEqual(len(restocked), 1)
        self.assertEqual(restocked[0]['part_id'], "P002")

    def test_total_inventory_value(self):
        self.manager.inventory_items.append(self.item)
        total_value = self.manager.calculate_total_inventory_value()
        self.assertEqual(total_value, 250.0)

class TestQualityControlManager(unittest.TestCase):
    def setUp(self):
        self.manager = QualityControlManager()
        self.address = Address("Test St", "City", "ST", "12345", "Country", "123")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        self.order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")

    def test_quality_inspection(self):
        criteria = ["Functionality", "Appearance", "Safety", "Performance", "Durability", "Workmanship"]
        passed = self.manager.perform_quality_inspection(self.order, None, criteria)
        self.assertTrue(passed)

    def test_quality_report(self):
        criteria = ["Functionality", "Appearance", "Safety"]
        self.manager.perform_quality_inspection(self.order, None, criteria)
        
        report = self.manager.generate_quality_report()
        self.assertIn("Quality Report", report)

if __name__ == '__main__':
    unittest.main()