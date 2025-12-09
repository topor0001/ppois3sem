import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.client import Client
from src.models.address import Address
from src.models.employee import Employee
from src.models.technician import Technician
from src.models.service import RepairService
from src.models.inventory import InventoryItem
from src.models.repair_order import RepairOrder
from src.models.payment import Payment
from src.models.warranty import Warranty
from src.models.warranty_claim import WarrantyClaim
from src.models.appointment import Appointment
from src.exceptions.insufficient_funds_exception import InsufficientFundsException
from src.exceptions.invalid_client_data_exception import InvalidClientDataException
from src.exceptions.order_not_found_exception import OrderNotFoundException
from src.exceptions.technician_not_available_exception import TechnicianNotAvailableException
from src.exceptions.part_not_available_exception import PartNotAvailableException
from src.exceptions.service_not_available_exception import ServiceNotAvailableException
from src.exceptions.invalid_payment_data_exception import InvalidPaymentDataException
from src.exceptions.warranty_expired_exception import WarrantyExpiredException
from src.exceptions import (
    InsufficientFundsException, InvalidClientDataException, OrderNotFoundException,
    TechnicianNotAvailableException, PartNotAvailableException, ServiceNotAvailableException,
    InvalidPaymentDataException, WarrantyExpiredException
)

from src.models.purchase_order import PurchaseOrder
from src.models.supplier import Supplier
from src.models.inventory import InventoryItem
class TestClient(unittest.TestCase):
    def setUp(self):
        self.address = Address("Main St", "New York", "NY", "10001", "USA", "123")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)

    def test_client_creation(self):
        self.assertEqual(self.client.client_id, "CL001")
        self.assertEqual(self.client.name, "John Doe")
        self.assertEqual(self.client.balance, 1000.0)

    def test_add_funds(self):
        self.client.add_funds(500.0)
        self.assertEqual(self.client.balance, 1500.0)

    def test_deduct_funds_success(self):
        result = self.client.deduct_funds(300.0)
        self.assertTrue(result)
        self.assertEqual(self.client.balance, 700.0)

    def test_deduct_funds_insufficient(self):
        with self.assertRaises(InsufficientFundsException):
            self.client.deduct_funds(2000.0)

    def test_transfer_to_another_client(self):
        client2 = Client("CL002", "Jane Doe", "jane@test.com", "+1987654321", self.address, 500.0)
        result = self.client.transfer_to_another_client(client2, 300.0)
        self.assertTrue(result)
        self.assertEqual(self.client.balance, 700.0)
        self.assertEqual(client2.balance, 800.0)

    def test_loyalty_points(self):
        self.client.add_loyalty_points(150)
        self.assertEqual(self.client.loyalty_points, 150)
        
        discount = self.client.calculate_discount()
        self.assertEqual(discount, 1)

    def test_loyalty_tier(self):
        self.client.add_loyalty_points(600)
        tier = self.client.calculate_loyalty_tier()
        self.assertEqual(tier, "SILVER")

    def test_invalid_client_data(self):
        with self.assertRaises(InvalidClientDataException):
            Client("", "John", "invalid-email", "123", self.address, 100.0)

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.address = Address("Work St", "Boston", "MA", "02101", "USA", "456")
        self.employee = Employee("EMP001", "Mike", "Johnson", "Technician", 50000.0, 
                               "2023-01-15", "Repair", self.address, "Electronics")

    def test_employee_creation(self):
        self.assertEqual(self.employee.employee_id, "EMP001")
        self.assertEqual(self.employee.get_full_name(), "Mike Johnson")
        self.assertTrue(self.employee.is_available)

    def test_assign_order(self):
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        order = RepairOrder("RO001", client, "Device", "Problem", service, None, "NORMAL", "2024-01-01")
        
        self.employee.assign_order(order)
        self.assertIn(order, self.employee.assigned_orders)
        self.assertFalse(self.employee.is_available)

    def test_complete_order(self):
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        order = RepairOrder("RO001", client, "Device", "Problem", service, None, "NORMAL", "2024-01-01")
        
        self.employee.assign_order(order)
        self.employee.complete_order(order)
        self.assertNotIn(order, self.employee.assigned_orders)
        self.assertTrue(self.employee.is_available)

class TestTechnician(unittest.TestCase):
    def setUp(self):
        self.address = Address("Tech St", "Seattle", "WA", "98101", "USA", "789")
        self.technician = Technician("T001", "Sarah", "Wilson", "Senior Technician", 60000.0,
                                   "2022-06-01", "Repair", self.address, "Electronics", 8, ["Cert1", "Cert2"])

    def test_technician_creation(self):
        self.assertEqual(self.technician.skill_level, 8)
        self.assertEqual(len(self.technician.tools_certification), 2)

    def test_efficiency_score(self):
        score = self.technician.calculate_efficiency_score()
        self.assertGreaterEqual(score, 0)

    def test_repair_stats_update(self):
        self.technician.update_repair_stats(2.5)
        self.assertEqual(self.technician.completed_repairs_count, 1)
        self.assertEqual(self.technician.average_repair_time, 2.5)

    def test_equipment_certification(self):
        self.technician.add_equipment_certification("New Equipment")
        self.assertIn("New Equipment", self.technician.specialized_equipment)

class TestRepairService(unittest.TestCase):
    def setUp(self):
        self.service = RepairService("S001", "Screen Replacement", "Replace broken screen", 
                                   150.0, 1.5, ["Screen", "Adhesive"], 6, 180)

    def test_service_creation(self):
        self.assertEqual(self.service.service_id, "S001")
        self.assertEqual(self.service.base_cost, 150.0)
        self.assertTrue(self.service.is_available)

    def test_final_cost_calculation(self):
        final_cost = self.service.calculate_final_cost(1.2, 1.0)
        expected_cost = 150.0 * 1.2
        self.assertEqual(final_cost, expected_cost)

    def test_technician_qualification(self):
        self.assertTrue(self.service.check_technician_qualification(7))
        self.assertFalse(self.service.check_technician_qualification(5))

    def test_invalid_service_data(self):
        with self.assertRaises(ServiceNotAvailableException):
            RepairService("", "", "", -100, 0, [], 0, 0)

class TestInventoryItem(unittest.TestCase):
    def setUp(self):
        self.item = InventoryItem("P001", "LCD Screen", "6.1 inch OLED", "Display", 
                                89.99, 25, 5, "Supplier Co", ["iPhone 14", "iPhone 15"])

    def test_inventory_creation(self):
        self.assertEqual(self.item.part_id, "P001")
        self.assertEqual(self.item.price, 89.99)
        self.assertEqual(self.item.quantity_in_stock, 25)

    def test_availability_check(self):
        self.assertTrue(self.item.check_availability(10))
        self.assertFalse(self.item.check_availability(30))

    def test_reserve_items(self):
        self.item.reserve_items(5)
        self.assertEqual(self.item.quantity_in_stock, 20)

    def test_reserve_insufficient_items(self):
        with self.assertRaises(PartNotAvailableException):
            self.item.reserve_items(30)

    def test_restock_items(self):
        self.item.restock_items(10)
        self.assertEqual(self.item.quantity_in_stock, 35)

    def test_needs_restocking(self):
        self.assertFalse(self.item.needs_restocking())
        
        low_stock_item = InventoryItem("P002", "Battery", "Li-ion", "Power", 
                                     45.99, 3, 5, "Supplier Co", [])
        self.assertTrue(low_stock_item.needs_restocking())

class TestRepairOrder(unittest.TestCase):
    def setUp(self):
        self.address = Address("Client St", "Chicago", "IL", "60601", "USA", "111")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.technician = Technician("T001", "Mike", "Tech", "Technician", 50000.0,
                                   "2023-01-01", "Repair", self.address, "Electronics", 7, [])
        self.service = RepairService("S001", "Test Service", "Description", 200.0, 2.0, [], 6, 90)
        self.order = RepairOrder("RO001", self.client, "iPhone 14", "Broken screen", 
                               self.service, self.technician, "HIGH", "2024-01-01")

    def test_order_creation(self):
        self.assertEqual(self.order.order_id, "RO001")
        self.assertEqual(self.order.status, "CREATED")
        self.assertEqual(self.order.priority_level, "HIGH")

    def test_add_used_part(self):
        part = InventoryItem("P001", "Screen", "OLED", "Display", 99.99, 10, 2, "Supplier", [])
        self.order.add_used_part(part, 1)
        self.assertEqual(len(self.order.used_parts), 1)
        self.assertEqual(part.quantity_in_stock, 9)

    def test_total_cost_calculation(self):
        part = InventoryItem("P001", "Screen", "OLED", "Display", 99.99, 10, 2, "Supplier", [])
        self.order.add_used_part(part, 1)
        self.order.actual_hours = 2.5
        
        total_cost = self.order.calculate_total_cost()
        self.assertGreater(total_cost, 0)

    def test_mark_in_progress(self):
        self.order.mark_in_progress()
        self.assertEqual(self.order.status, "IN_PROGRESS")

    def test_mark_completed(self):
        self.order.mark_completed(2.5)
        self.assertEqual(self.order.status, "COMPLETED")
        self.assertEqual(self.order.actual_hours, 2.5)

class TestPayment(unittest.TestCase):
    def setUp(self):
        self.address = Address("Pay St", "Miami", "FL", "33101", "USA", "222")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.service = RepairService("S001", "Test Service", "Description", 300.0, 1.0, [], 5, 90)
        self.order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")
        self.payment = Payment("PAY001", self.client, self.order, 350.0, "CREDIT_CARD", "2024-01-01")

    def test_payment_creation(self):
        self.assertEqual(self.payment.payment_id, "PAY001")
        self.assertEqual(self.payment.amount, 350.0)
        self.assertFalse(self.payment.is_processed)

    def test_process_payment(self):
        result = self.payment.process_payment()
        self.assertTrue(result)
        self.assertTrue(self.payment.is_processed)
        self.assertEqual(self.client.balance, 650.0)

    def test_process_payment_insufficient_funds(self):
        poor_client = Client("CL002", "Poor Client", "poor@test.com", "+1234567890", self.address, 100.0)
        payment = Payment("PAY002", poor_client, self.order, 350.0, "CREDIT_CARD", "2024-01-01")
        
        with self.assertRaises(InsufficientFundsException):
            payment.process_payment()

    def test_generate_receipt(self):
        self.payment.process_payment()
        receipt = self.payment.generate_receipt()
        self.assertIn("PAYMENT RECEIPT", receipt)
        self.assertIn("PAY001", receipt)

    def test_invalid_payment_data(self):
        with self.assertRaises(InvalidPaymentDataException):
            Payment("", None, None, -100, "", "")

class TestWarranty(unittest.TestCase):
    def setUp(self):
        self.address = Address("Test St", "City", "ST", "12345", "Country", "123")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        self.order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")
        self.warranty = Warranty("W001", self.order, 90, "2024-01-01", "Standard terms")

    def test_warranty_creation(self):
        self.assertEqual(self.warranty.warranty_id, "W001")
        self.assertTrue(self.warranty.is_valid())

    def test_claim_registration(self):
        self.warranty.register_claim()
        self.assertEqual(self.warranty.claims_count, 1)
        
        self.warranty.register_claim()
        self.warranty.register_claim()
        self.assertFalse(self.warranty.is_valid())

class TestWarrantyClaim(unittest.TestCase):
    def setUp(self):
        self.address = Address("Test St", "City", "ST", "12345", "Country", "123")
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", self.address, 1000.0)
        self.service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        self.order = RepairOrder("RO001", self.client, "Device", "Problem", self.service, None, "NORMAL", "2024-01-01")
        self.warranty = Warranty("W001", self.order, 90, "2024-01-01", "Standard terms")
        self.claim = WarrantyClaim("C001", self.warranty, self.order, "2024-01-15", "Device stopped working", [])

    def test_claim_evaluation_valid(self):
        result = self.claim.evaluate_claim(None)
        self.assertTrue(result)
        self.assertEqual(self.claim.status, "APPROVED")

    def test_claim_evaluation_invalid(self):
        self.warranty.claims_count = 3
        result = self.claim.evaluate_claim(None)
        self.assertFalse(result)
        self.assertEqual(self.claim.status, "REJECTED")
class TestPurchaseOrder(unittest.TestCase):
    
    def setUp(self):
        from src.models.supplier import Supplier
        from src.models.inventory import InventoryItem
        
        self.supplier = Supplier("SUP001", "Test Supplier", "John Smith", 
                                "+1234567890", "john@supplier.com", None, 4.5)
        
        self.item1 = InventoryItem("P001", "Test Part 1", "Description 1", 
                                  "Category A", 25.0, 10, 5, self.supplier, [])
        self.item2 = InventoryItem("P002", "Test Part 2", "Description 2", 
                                  "Category B", 50.0, 20, 10, self.supplier, [])
        
        self.order = PurchaseOrder("PO001", self.supplier, 
                                  [self.item1, self.item2], 
                                  "2024-01-15", "2024-01-30", 1250.0)
    
    def test_purchase_order_creation(self):
        self.assertEqual(self.order.order_id, "PO001")
        self.assertEqual(self.order.supplier, self.supplier)
        self.assertEqual(len(self.order.items), 2)
        self.assertEqual(self.order.order_date, "2024-01-15")
        self.assertEqual(self.order.expected_delivery, "2024-01-30")
        self.assertEqual(self.order.total_amount, 1250.0)
        self.assertEqual(self.order.status, "PENDING")
        self.assertEqual(len(self.order.received_items), 0)
    
def test_process_delivery_partial(self):
    delivered_items = [
        {'item': self.item1, 'quantity': 5},
        {'item': self.item2, 'quantity': 10}
    ]
    
    self.order.process_delivery(delivered_items)
    self.assertEqual(self.order.status, "PENDING")
    
    def test_process_delivery_complete(self):
        delivered_items = [
            {'item': self.item1, 'quantity': 1},
            {'item': self.item2, 'quantity': 1}
        ]
        
        self.order.process_delivery(delivered_items)
        
        self.assertEqual(self.order.status, "COMPLETED")
        self.assertEqual(len(self.order.received_items), 2)
    
    def test_process_delivery_single_item(self):
        delivered_items = [
            {'item': self.item1, 'quantity': 3}
        ]
        
        self.order.process_delivery(delivered_items)
        
        self.assertEqual(len(self.order.received_items), 1)
        self.assertEqual(self.order.status, "PENDING")
    
    def test_process_delivery_empty(self):
        delivered_items = []
        
        self.order.process_delivery(delivered_items)
        
        self.assertEqual(len(self.order.received_items), 0)
        self.assertEqual(self.order.status, "PENDING")
    
    def test_purchase_order_with_single_item(self):
        order = PurchaseOrder("PO002", self.supplier, [self.item1], 
                             "2024-01-16", "2024-01-31", 250.0)
        
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.total_amount, 250.0)
    
    def test_purchase_order_with_empty_items(self):
        order = PurchaseOrder("PO003", self.supplier, [], 
                             "2024-01-17", "2024-02-01", 0.0)
        
        self.assertEqual(len(order.items), 0)
        self.assertEqual(order.total_amount, 0.0)

class TestSupplierExtended(unittest.TestCase):
    def setUp(self):
        self.address = Address("Supplier St", "City", "ST", "12345", 
                              "Country", "123")
        self.supplier = Supplier("SUP001", "TechParts Inc", "John Smith", 
                                "+1987654321", "john@techparts.com", 
                                self.address, 4.5)
    
    def test_supplier_creation(self):
        self.assertEqual(self.supplier.supplier_id, "SUP001")
        self.assertEqual(self.supplier.name, "TechParts Inc")
        self.assertEqual(self.supplier.contact_person, "John Smith")
        self.assertEqual(self.supplier.phone, "+1987654321")
        self.assertEqual(self.supplier.email, "john@techparts.com")
        self.assertEqual(self.supplier.address, self.address)
        self.assertEqual(self.supplier.rating, 4.5)
        self.assertEqual(self.supplier.delivery_time_days, 7)
    
    def test_calculate_reliability_score(self):
        score = self.supplier.calculate_reliability_score()
        self.assertEqual(score, 90.0)  # 4.5 * 20
    
    def test_calculate_reliability_score_max(self):
        supplier = Supplier("SUP002", "Best Supplier", "Jane Doe", 
                          "+1234567890", "jane@best.com", None, 5.0)
        score = supplier.calculate_reliability_score()
        self.assertEqual(score, 100.0)  # 5.0 * 20
    
    def test_calculate_reliability_score_min(self):
        supplier = Supplier("SUP003", "Worst Supplier", "Bob Smith", 
                          "+0987654321", "bob@worst.com", None, 1.0)
        score = supplier.calculate_reliability_score()
        self.assertEqual(score, 20.0)  # 1.0 * 20
class TestTechnicianExtended(unittest.TestCase):
    
    def setUp(self):
        self.address = Address("Tech St", "City", "ST", "12345", 
                              "Country", "123")
        self.technician = Technician("T001", "Sarah", "Wilson", "Senior Technician", 
                                   60000.0, "2022-06-01", "Repair", 
                                   self.address, "Electronics", 8, ["Cert1", "Cert2"])
    
    def test_calculate_work_efficiency(self):
        class MockOrder:
            def __init__(self, status):
                self.status = status
        
        orders = [
            MockOrder("COMPLETED"),
            MockOrder("COMPLETED"),
            MockOrder("IN_PROGRESS"),
            MockOrder("CANCELLED")
        ]
        efficiency = self.technician.calculate_work_efficiency(orders, 10)
        self.assertEqual(efficiency, 0.2)  
        efficiency = self.technician.calculate_work_efficiency(orders, 0)
        self.assertEqual(efficiency, 0)
        efficiency = self.technician.calculate_work_efficiency(orders, -5)
        self.assertEqual(efficiency, 0)
    
    def test_find_compatible_services(self):
        class MockService:
            def __init__(self, name, skill_required):
                self.name = name
                self.skill_level_required = skill_required
        
        services = [
            MockService("Basic Repair", 5),
            MockService("Advanced Repair", 8),
            MockService("Expert Repair", 10),
            MockService("Simple Fix", 3)
        ]
        
        compatible = self.technician.find_compatible_services(services)
        self.assertEqual(len(compatible), 3)
        self.assertEqual(compatible[0].name, "Basic Repair")
        self.assertEqual(compatible[1].name, "Advanced Repair")
        self.assertEqual(compatible[2].name, "Simple Fix")
    
    def test_update_quality_rating(self):
        initial_rating = self.technician.quality_rating
        self.technician.update_quality_rating(4.5)
        self.assertEqual(self.technician.quality_rating, 4.5)
        self.technician.update_quality_rating(10.0)  
        self.assertEqual(self.technician.quality_rating, 4.5)  
        
        self.technician.update_quality_rating(0.0)   
        self.assertEqual(self.technician.quality_rating, 4.5)  
    
    def test_calculate_productivity(self):
        self.technician.completed_repairs_count = 25
        self.technician.average_repair_time = 2.5
        
        productivity = self.technician.calculate_productivity("2024-01-01", "2024-06-30")
        self.assertEqual(productivity, 290.0)
        self.technician.average_repair_time = 0
        productivity = self.technician.calculate_productivity("2024-01-01", "2024-06-30")
        self.assertEqual(productivity, 250.0)
    
    def test_request_tools(self):
        class MockToolManager:
            pass
        
        tool_manager = MockToolManager()
        request = self.technician.request_tools("Oscilloscope", tool_manager)
        
        self.assertIsInstance(request, dict)
        self.assertEqual(request['technician_id'], "T001")
        self.assertEqual(request['technician_name'], "Sarah Wilson")
        self.assertEqual(request['tool_name'], "Oscilloscope")
        self.assertEqual(request['status'], 'PENDING')
    
    def test_update_certifications(self):
        initial_certs = self.technician.tools_certification.copy()
        new_certs = ["Cert3", "Cert4", "Cert2"] 
        
        self.technician.update_certifications(new_certs)
        self.assertEqual(len(self.technician.tools_certification), 4)
        self.assertIn("Cert1", self.technician.tools_certification)
        self.assertIn("Cert2", self.technician.tools_certification)
        self.assertIn("Cert3", self.technician.tools_certification)
        self.assertIn("Cert4", self.technician.tools_certification)
    
    def test_generate_work_report(self):
        self.technician.completed_repairs_count = 42
        self.technician.average_repair_time = 3.75
        self.technician.efficiency_score = 88.5
        self.technician.quality_rating = 4.7
        self.technician.current_workload = 5
        
        report = self.technician.generate_work_report("2024-01-01", "2024-12-31")
        
        self.assertIsInstance(report, str)
        self.assertIn("Work Report for Sarah Wilson", report)
        self.assertIn("Period: 2024-01-01 to 2024-12-31", report)
        self.assertIn("Completed Repairs: 42", report)
        self.assertIn("Average Repair Time: 3.75", report)
        self.assertIn("Efficiency Score: 88.50", report)
        self.assertIn("Quality Rating: 4.7/5.0", report)
        self.assertIn("Current Workload: 5 orders", report)
    
    def test_validate_skills(self):
        required_skills = ["Cert1", "Cert3", "Cert5", "Cert7"]
        
        missing = self.technician.validate_skills(required_skills)
        self.assertEqual(len(missing), 3)
        self.assertIn("Cert3", missing)
        self.assertIn("Cert5", missing)
        self.assertIn("Cert7", missing)
        self.assertNotIn("Cert1", missing)
        self.assertNotIn("Cert2", missing)
    
    def test_can_handle_complex_repair(self):
        self.assertEqual(self.technician.skill_level, 8)
        
        self.assertTrue(self.technician.can_handle_complex_repair(8)) 
        self.assertTrue(self.technician.can_handle_complex_repair(5)) 
        self.assertFalse(self.technician.can_handle_complex_repair(10)) 
        self.assertFalse(self.technician.can_handle_complex_repair(9)) 
    
    def test_calculate_training_needs(self):
        required_certifications = ["Cert1", "Cert2", "Cert5", "Cert8", "Cert9"]
        
        needed = self.technician.calculate_training_needs(required_certifications)
        self.assertEqual(len(needed), 3)
        self.assertIn("Cert5", needed)
        self.assertIn("Cert8", needed)
        self.assertIn("Cert9", needed)
        self.assertNotIn("Cert1", needed)
        self.assertNotIn("Cert2", needed)
if __name__ == '__main__':
    unittest.main()