import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.client import Client
from src.models.address import Address
from src.models.technician import Technician
from src.models.service import RepairService
from src.models.repair_order import RepairOrder
from src.models.inventory import InventoryItem
from src.models.payment import Payment
from src.finance.bank_account import BankAccount
from src.services.repair_service import RepairServiceManager

class TestIntegrationScenarios(unittest.TestCase):
    def test_complete_repair_workflow(self):
        # Setup
        address = Address("123 Main St", "New York", "NY", "10001", "USA", "1A")
        client = Client("CL001", "John Smith", "john@example.com", "+1234567890", address, 2000.0)
        technician = Technician("T001", "Mike", "Johnson", "Technician", 50000.0,
                              "2023-01-01", "Repair", address, "Electronics", 7, [])
        service = RepairService("S001", "Screen Repair", "Fix broken screen", 300.0, 1.5, [], 6, 90)
        inventory_item = InventoryItem("P001", "OLED Screen", "6.1 inch", "Display", 150.0, 10, 2, "Supplier", [])
        
        # Create order
        order = RepairOrder("RO001", client, "iPhone 14", "Cracked screen", service, technician, "HIGH", "2024-01-01")
        
        # Add parts and process
        order.add_used_part(inventory_item, 1)
        order.mark_in_progress()
        order.mark_completed(2.0)
        total_cost = order.calculate_total_cost()
        
        # Process payment
        payment = Payment("PAY001", client, order, total_cost, "CREDIT_CARD", "2024-01-02")
        payment.process_payment()
        
        # Verify results
        self.assertEqual(order.status, "COMPLETED")
        self.assertTrue(payment.is_processed)
        self.assertLess(client.balance, 2000.0)
        self.assertEqual(inventory_item.quantity_in_stock, 9)

    def test_bank_transfer_integration(self):
        client1 = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 5000.0)
        client2 = Client("CL002", "Jane Doe", "jane@test.com", "+1987654321", None, 3000.0)
        
        account1 = BankAccount("ACC001", client1, "Bank", 5000.0, "USD")
        account2 = BankAccount("ACC002", client2, "Bank", 3000.0, "USD")
        
        # Transfer money
        account1.transfer_to_another_account(account2, 1000.0)
        
        # Verify transfer
        self.assertEqual(account1.balance, 4000.0)
        self.assertEqual(account2.balance, 4000.0)
        self.assertEqual(len(account1.transaction_history), 1)

    def test_repair_service_manager_integration(self):
        manager = RepairServiceManager()
        address = Address("Test St", "City", "ST", "12345", "Country", "123")
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", address, 1000.0)
        technician = Technician("T001", "Tech", "Nician", "Technician", 50000.0,
                              "2023-01-01", "Repair", address, "Electronics", 7, [])
        service = RepairService("S001", "Test Service", "Description", 100.0, 1.0, [], 5, 90)
        
        # Add technician to available list
        manager.available_technicians.append(technician)
        
        # Create and assign order
        order = RepairOrder("RO001", client, "Device", "Problem", service, None, "NORMAL", "2024-01-01")
        manager.active_orders.append(order)
        
        manager.assign_technician_to_order("RO001", technician)
        
        # Complete order
        part = InventoryItem("P001", "Part", "Description", "Category", 50.0, 10, 2, "Supplier", [])
        used_parts = [{'part': part, 'quantity': 1}]
        
        total_cost = manager.complete_repair_order("RO001", 2.0, used_parts)
        
        # Verify completion
        self.assertGreater(total_cost, 0)
        self.assertEqual(order.status, "COMPLETED")
        self.assertIn(order, manager.completed_orders)
        self.assertNotIn(order, manager.active_orders)

    def test_client_loyalty_integration(self):
        address = Address("123 St", "City", "ST", "12345", "Country", "123")
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", address, 1000.0)
        
        # Simulate multiple repairs
        for i in range(5):
            service = RepairService(f"SRV{i}", f"Service {i}", "Description", 200.0, 1.0, [], 5, 90)
            order = RepairOrder(f"RO{i}", client, "Device", "Problem", service, None, "NORMAL", "2024-01-01")
            
            # Add loyalty points for each repair
            client.add_loyalty_points(50)
            client.repair_history.append(order)
        
        # Check loyalty benefits
        self.assertEqual(client.loyalty_points, 250)
        self.assertEqual(client.calculate_discount(), 2)
        self.assertEqual(client.calculate_loyalty_tier(), "BRONZE")
        self.assertEqual(len(client.repair_history), 5)

if __name__ == '__main__':
    unittest.main()