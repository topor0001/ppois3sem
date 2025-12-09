import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.appointment import Appointment
from src.models.service_package import ServicePackage
from src.models.supplier import Supplier
from src.models.service_category import ServiceCategory
from src.models.manager import Manager
from src.models.receptionist import Receptionist
from src.models.purchase_order import PurchaseOrder
from src.models.quality_inspection import QualityInspection
from src.models.client import Client
from src.models.address import Address
from src.models.employee import Employee
from src.models.service import RepairService

class TestAppointment(unittest.TestCase):
    def setUp(self):
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        self.technician = Employee("T001", "Mike", "Johnson", "Technician", 50000.0,
                                 "2023-01-01", "Repair", None, "Electronics")
    
    def test_appointment_creation(self):
        appointment = Appointment("APT001", self.client, self.technician, 
                                 "2024-01-15", 2.0, "Screen Repair")
        
        self.assertEqual(appointment.appointment_id, "APT001")
        self.assertEqual(appointment.client, self.client)
        self.assertEqual(appointment.technician, self.technician)
        self.assertEqual(appointment.scheduled_date, "2024-01-15")
        self.assertEqual(appointment.duration_hours, 2.0)
        self.assertEqual(appointment.service_type, "Screen Repair")
        self.assertEqual(appointment.status, "SCHEDULED")
    
    def test_appointment_reschedule(self):
        appointment = Appointment("APT001", self.client, self.technician, 
                                 "2024-01-15", 2.0, "Screen Repair")
        
        appointment.reschedule("2024-01-20")
        self.assertEqual(appointment.scheduled_date, "2024-01-20")

class TestServicePackage(unittest.TestCase):
    def setUp(self):
        self.service1 = RepairService("SRV001", "Screen Repair", "Fix screen", 100.0, 1.0, [], 5, 90)
        self.service2 = RepairService("SRV002", "Battery Replace", "Replace battery", 80.0, 0.5, [], 4, 90)
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
    
    def test_service_package_creation(self):
        package = ServicePackage("PKG001", "Premium Package", "All services",
                                [self.service1, self.service2], 20.0, 365)
        
        self.assertEqual(package.package_id, "PKG001")
        self.assertEqual(package.name, "Premium Package")
        self.assertEqual(len(package.included_services), 2)
        self.assertEqual(package.discount_rate, 20.0)
        self.assertEqual(package.validity_period, 365)
    
    def test_calculate_package_price(self):
        package = ServicePackage("PKG001", "Premium Package", "All services",
                                [self.service1, self.service2], 20.0, 365)
        
        price = package.calculate_package_price()
        expected = (100.0 + 80.0) * (1 - 20.0/100)
        self.assertEqual(price, expected)
    
    def test_add_client_to_package(self):
        package = ServicePackage("PKG001", "Premium Package", "All services",
                                [self.service1, self.service2], 20.0, 365)
        
        # Add client
        result = package.add_client_to_package(self.client)
        self.assertTrue(result)
        self.assertIn(self.client, package.active_clients)
        
        # Try to add same client again
        result = package.add_client_to_package(self.client)
        self.assertFalse(result)

class TestSupplier(unittest.TestCase):
    def setUp(self):
        self.address = Address("Supplier St", "City", "ST", "12345", "Country", "123")
    
    def test_supplier_creation(self):
        supplier = Supplier("SUP001", "TechParts Inc", "John Smith", "+1987654321",
                          "john@techparts.com", self.address, 4.5)
        
        self.assertEqual(supplier.supplier_id, "SUP001")
        self.assertEqual(supplier.name, "TechParts Inc")
        self.assertEqual(supplier.contact_person, "John Smith")
        self.assertEqual(supplier.phone, "+1987654321")
        self.assertEqual(supplier.email, "john@techparts.com")
        self.assertEqual(supplier.address, self.address)
        self.assertEqual(supplier.rating, 4.5)
        self.assertEqual(supplier.delivery_time_days, 7)
    
    def test_calculate_reliability_score(self):
        supplier = Supplier("SUP001", "TechParts Inc", "John Smith", "+1987654321",
                          "john@techparts.com", self.address, 4.5)
        
        score = supplier.calculate_reliability_score()
        self.assertEqual(score, 4.5 * 20)  # 90.0

class TestServiceCategory(unittest.TestCase):
    def test_service_category_creation(self):
        service1 = RepairService("SRV001", "Service1", "Desc1", 100.0, 1.0, [], 5, 90)
        service2 = RepairService("SRV002", "Service2", "Desc2", 150.0, 2.0, [], 6, 120)
        
        category = ServiceCategory("CAT001", "Electronics", "Electronic repairs",
                                  None, [service1, service2])
        
        self.assertEqual(category.category_id, "CAT001")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(len(category.services), 2)
        self.assertIsNone(category.parent_category)
    
    def test_get_all_services_recursive(self):
        service1 = RepairService("SRV001", "Service1", "Desc1", 100.0, 1.0, [], 5, 90)
        service2 = RepairService("SRV002", "Service2", "Desc2", 150.0, 2.0, [], 6, 120)
        service3 = RepairService("SRV003", "Service3", "Desc3", 200.0, 3.0, [], 7, 150)
        
        parent_category = ServiceCategory("CAT001", "Parent", "Parent category",
                                         None, [service1])
        child_category = ServiceCategory("CAT002", "Child", "Child category",
                                        parent_category, [service2, service3])
        
        all_services = child_category.get_all_services_recursive()
        self.assertEqual(len(all_services), 3)  # service2 + service3 + service1 (from parent)
    
def test_calculate_category_revenue(self):
    service1 = RepairService("SRV001", "Screen Repair", "Fix screen", 100.0, 1.0, [], 5, 90)
    service2 = RepairService("SRV002", "Battery", "Replace battery", 150.0, 2.0, [], 6, 120)
    category = ServiceCategory("CAT001", "Electronics", "Electronic repairs", None, [service1, service2])
    
 
    print(f"Service 1 name: '{service1.name}', length: {len(service1.name)}")
    print(f"Service 2 name: '{service2.name}', length: {len(service2.name)}")
    print(f"Sum of lengths: {len(service1.name) + len(service2.name)}")
    
    revenue = category.calculate_category_revenue("2024-01-01", "2024-01-31")
    

    print(f"Calculated revenue: {revenue}")
    print(f"Expected: 1900, Got: {revenue}")
    
    self.assertEqual(revenue, 1900)

class TestManager(unittest.TestCase):
    def setUp(self):
        self.address = Address("Work St", "City", "ST", "12345", "Country", "123")
        self.employee = Employee("EMP001", "John", "Doe", "Technician", 50000.0,
                               "2023-01-01", "Repair", self.address, "Electronics")
        self.manager = Manager("MGR001", "Jane", "Smith", "Manager", 70000.0,
                             "2022-01-01", "Management", self.address, "Administration",
                             5, 100000.0)
    
    def test_manager_creation(self):
        self.assertEqual(self.manager.team_size, 5)
        self.assertEqual(self.manager.budget_responsibility, 100000.0)
        self.assertEqual(len(self.manager.managed_employees), 0)
        self.assertEqual(len(self.manager.approved_orders), 0)
    
    def test_assign_employee_to_department(self):
        self.manager.assign_employee_to_department(self.employee, "Repair Department")
        self.assertEqual(self.employee.department, "Repair Department")
        self.assertIn(self.employee, self.manager.managed_employees)
    
    def test_calculate_team_productivity(self):
        # Add employee to managed list
        self.manager.managed_employees.append(self.employee)
        
        productivity = self.manager.calculate_team_productivity()
        # employee has 0 assigned orders, team_size = 5
        # 0 / 5 = 0
        self.assertEqual(productivity, 0)

class TestReceptionist(unittest.TestCase):
    def setUp(self):
        self.address = Address("Work St", "City", "ST", "12345", "Country", "123")
        self.receptionist = Receptionist("REC001", "Sarah", "Jones", "Receptionist", 35000.0,
                                       "2023-03-01", "Front Desk", self.address, "Customer Service",
                                       "9AM-5PM", ["English", "Spanish"])
    
    def test_receptionist_creation(self):
        self.assertEqual(self.receptionist.shift_schedule, "9AM-5PM")
        self.assertEqual(self.receptionist.languages, ["English", "Spanish"])
        self.assertEqual(len(self.receptionist.processed_appointments), 0)
    
    def test_handle_phone_inquiry(self):
        response = self.receptionist.handle_phone_inquiry("John Smith", "pricing")
        expected = "Handled phone inquiry from John Smith about: pricing"
        self.assertEqual(response, expected)
    
    def test_generate_daily_schedule(self):
        # Add a test appointment
        from src.models.appointment import Appointment
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        appointment = Appointment("APT001", client, None, "2024-01-15", 2.0, "Consultation")
        self.receptionist.processed_appointments.append(appointment)
        
        schedule = self.receptionist.generate_daily_schedule("2024-01-15")
        self.assertIn("Schedule for 2024-01-15: 1 appointments", schedule)

class TestPurchaseOrder(unittest.TestCase):
    def test_purchase_order_creation(self):
        from src.models.supplier import Supplier
        from src.models.inventory import InventoryItem
        
        supplier = Supplier("SUP001", "TechParts", "John", "+1234567890", 
                          "john@techparts.com", None, 4.5)
        item = InventoryItem("P001", "Screwdriver", "Tool", "Tools", 15.99, 10, 5, supplier, [])
        
        order = PurchaseOrder("PO001", supplier, [item], "2024-01-15", "2024-01-22", 159.90)
        
        self.assertEqual(order.order_id, "PO001")
        self.assertEqual(order.supplier, supplier)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.order_date, "2024-01-15")
        self.assertEqual(order.expected_delivery, "2024-01-22")
        self.assertEqual(order.total_amount, 159.90)
        self.assertEqual(order.status, "PENDING")
        self.assertEqual(len(order.received_items), 0)

class TestQualityInspection(unittest.TestCase):
    def test_quality_inspection(self):
        from src.models.repair_order import RepairOrder
        from src.models.client import Client
        
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        order = RepairOrder("RO001", client, "Device", "Problem", None, None, "NORMAL", "2024-01-01")
        
        criteria = ["Functionality", "Safety", "Appearance", "Performance", "Durability", "Workmanship"]
        inspection = QualityInspection("INS001", order, "Inspector1", "2024-01-02", criteria)
        
        self.assertEqual(inspection.inspection_id, "INS001")
        self.assertEqual(inspection.repair_order, order)
        self.assertEqual(inspection.inspector, "Inspector1")
        self.assertEqual(inspection.inspection_date, "2024-01-02")
        self.assertEqual(inspection.criteria, criteria)
        self.assertFalse(inspection.passed)
    
    def test_perform_inspection(self):
        from src.models.repair_order import RepairOrder
        from src.models.client import Client
        
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        order = RepairOrder("RO001", client, "Device", "Problem", None, None, "NORMAL", "2024-01-01")
        
        # Test with 6 criteria (should pass)
        criteria = ["F1", "F2", "F3", "F4", "F5", "F6"]
        inspection = QualityInspection("INS001", order, "Inspector1", "2024-01-02", criteria)
        inspection.perform_inspection()
        self.assertTrue(inspection.passed)
        
        # Test with 4 criteria (should fail)
        criteria2 = ["F1", "F2", "F3", "F4"]
        inspection2 = QualityInspection("INS002", order, "Inspector1", "2024-01-02", criteria2)
        inspection2.perform_inspection()
        self.assertFalse(inspection2.passed)

if __name__ == '__main__':
    unittest.main()