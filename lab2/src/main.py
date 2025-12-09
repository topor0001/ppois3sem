from src.models.client import Client
from src.models.address import Address
from src.models.technician import Technician
from src.models.service import RepairService
from src.models.repair_order import RepairOrder
from src.models.inventory import InventoryItem
from src.models.payment import Payment
from src.finance.bank_account import BankAccount
from src.security.user_account import UserAccount
from src.services.repair_service import RepairServiceManager
from src.services.inventory_service import InventoryManager
from src.utils import manual_utils_instance as ManualUtils

class RepairCompanyDemo:
    def __init__(self):
        self.clients = []
        self.employees = []
        self.services = []
        self.orders = []
        self.payments = []

    def demonstrate_all_functionality(self):
        print("=== REPAIR COMPANY SYSTEM DEMONSTRATION ===\n")
        
        self._create_sample_data()
        
        self._demonstrate_client_behaviors()
        self._demonstrate_payment_behaviors()
        self._demonstrate_employee_behaviors()
        self._demonstrate_banking_behaviors()
        self._demonstrate_security_behaviors()
        self._demonstrate_manual_functions()
        
        print("\n=== ALL FUNCTIONALITIES DEMONSTRATED ===")

    def _create_sample_data(self):
        client_address = Address("123 Main St", "New York", "NY", "10001", "USA", "15A")
        company_address = Address("456 Business Ave", "New York", "NY", "10002", "USA", "Suite 200")
        
        client = Client("CL001", "John Smith", "john.smith@email.com", "+1234567890", client_address, 2500.0)
        self.clients.append(client)
        
        technician = Technician("T001", "Mike", "Johnson", "Senior Technician", 55000.0,
                              "2022-03-15", "Repair", company_address, "Electronics", 8, 
                              ["Soldering", "Diagnostics", "Microsoldering"])
        self.employees.append(technician)
        
        service = RepairService("SRV001", "Screen Replacement", "Replace broken smartphone screen", 
                              300.0, 1.5, ["OLED Screen", "Adhesive", "Tools"], 6, 180)
        self.services.append(service)

    def _demonstrate_client_behaviors(self):
        print("1. CLIENT BEHAVIORS:")
        client = self.clients[0]
        
        client.add_funds(500.0)
        print(f" - Added funds: ${500.0:.2f} → Balance: ${client.balance:.2f}")
        
        try:
            client.deduct_funds(800.0)
            print(f" - Deducted funds: ${800.0:.2f} → Balance: ${client.balance:.2f}")
        except Exception as e:
            print(f" - Deduction error: {e}")
        
        client2 = Client("CL002", "Maria Garcia", "maria.garcia@email.com", "+1987654321", 
                        self.clients[0].address, 1500.0)
        print(f" - Created second client: {client2.name}")
        
        client.add_loyalty_points(250)
        discount = client.calculate_discount()
        print(f" - Loyalty discount: {discount}%")
        
        tier = client.calculate_loyalty_tier()
        print(f" - Loyalty tier: {tier}")

    def _demonstrate_payment_behaviors(self):
        print("\n2. PAYMENT BEHAVIORS:")
        client = self.clients[0]
        service = self.services[0]
        
        order = RepairOrder("RO001", client, "iPhone 14 Pro", "Cracked OLED screen", 
                          service, self.employees[0], "HIGH", "2024-01-15")
        self.orders.append(order)
        
        order.add_used_part(InventoryItem("SCR001", "OLED Screen", "6.1 inch", "Display", 
                                        189.99, 50, 5, "ScreenCo", ["iPhone 14 Pro"]), 1)
        order.actual_hours = 1.2
        total_cost = order.calculate_total_cost()
        
        payment = Payment("PAY001", client, order, total_cost, "CREDIT_CARD", "2024-01-15")
        
        try:
            payment.process_payment()
            print(f" - Payment processed: ${total_cost:.2f}")
            self.payments.append(payment)
            
            receipt = payment.generate_receipt()
            print(" - Receipt generated successfully")
            
        except Exception as e:
            print(f" - Payment error: {e}")
        
        installments = payment.process_installment_plan(3)
        print(f" - Installment plan: 3 payments of ${installments[0]:.2f}")

    def _demonstrate_employee_behaviors(self):
        print("\n3. EMPLOYEE BEHAVIORS:")
        technician = self.employees[0]
        
        order = self.orders[0]
        try:
            technician.assign_order(order)
            print(f" - Order assigned to technician: {technician.get_full_name()}")
        except Exception as e:
            print(f" - Assignment error: {e}")
        
        efficiency = technician.calculate_efficiency_score()
        print(f" - Technician efficiency score: {efficiency:.2f}")
        
        technician.add_equipment_certification("Laser Welder")
        print(f" - Added equipment certification: Laser Welder")
        
        compatible_services = technician.find_compatible_services(self.services)
        print(f" - Compatible services: {len(compatible_services)}")

    def _demonstrate_banking_behaviors(self):
        print("\n4. BANKING BEHAVIORS:")
        client_account = BankAccount("40817810099910004312", self.clients[0], "Main Bank", 5000.0, "USD")
        company_account = BankAccount("40702810500000012345", None, "Main Bank", 100000.0, "USD")
        
        try:
            client_account.transfer_to_another_account(company_account, 1500.0)
            print(f" - Transfer completed: ${1500.0:.2f} USD")
            print(f" - Client balance: ${client_account.balance:.2f}")
            print(f" - Company balance: ${company_account.balance:.2f}")
            
            stats = client_account.get_transaction_statistics()
            print(f" - Transaction stats: {stats['count']} transactions, total: ${stats['total']:.2f}")
            
        except Exception as e:
            print(f" - Transfer error: {e}")
        
        interest = client_account.calculate_interest(5.0, 30)
        print(f" - Monthly interest (5%): ${interest:.2f}")

    def _demonstrate_security_behaviors(self):
        print("\n5. SECURITY BEHAVIORS:")
        user = UserAccount("U001", "john_smith", 123456789, "john@email.com", "CLIENT", "2024-01-01", None)
        
        password_strength = user.validate_password_strength("StrongPass123!")
        print(f" - Password strength check: {'Strong' if password_strength else 'Weak'}")
        
        verification = user.verify_password("testpassword")
        print(f" - Password verification: {'Success' if verification else 'Failed'}")
        
        lock_status = user.check_account_lock_status()
        print(f" - Account lock status: {'Locked' if lock_status else 'Active'}")
        
        recovery_token = user.generate_password_recovery_token()
        print(f" - Recovery token generated: {recovery_token}")

    def _demonstrate_manual_functions(self):
        print("\n6. MANUAL FUNCTIONS DEMONSTRATION:")
        
        numbers = [15, 3, 28, 7, 42, 9]
        manual_sum = ManualUtils.manual_sum(numbers)
        manual_max = ManualUtils.manual_max(numbers)
        manual_min = ManualUtils.manual_min(numbers)
        
        print(f" - manual_sum({numbers}) = {manual_sum}")
        print(f" - manual_max({numbers}) = {manual_max}")
        print(f" - manual_min({numbers}) = {manual_min}")
        
        manual_range = ManualUtils.manual_range(1, 6)
        print(f" - manual_range(1, 6) = {manual_range}")
        
        manual_sorted = ManualUtils.manual_sorted([34, 12, 56, 7, 23])
        print(f" - manual_sorted([34, 12, 56, 7, 23]) = {manual_sorted}")
        
        manual_abs = ManualUtils.manual_abs(-15.75)
        print(f" - manual_abs(-15.75) = {manual_abs}")
        
        manual_round = ManualUtils.manual_round(3.14159, 2)
        print(f" - manual_round(3.14159, 2) = {manual_round}")

if __name__ == "__main__":
    demo = RepairCompanyDemo()
    demo.demonstrate_all_functionality()