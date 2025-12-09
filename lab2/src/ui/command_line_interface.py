from src.ui import input_handler_instance as InputHandler
from src.models.client import Client
from src.models.address import Address
from src.models.technician import Technician
from src.models.service import RepairService
from src.models.repair_order import RepairOrder
from src.models.inventory import InventoryItem
from src.models.payment import Payment
from src.models.appointment import Appointment
from src.models.warranty import Warranty
from src.finance.bank_account import BankAccount
from src.finance.invoice import Invoice
from src.services.repair_service import RepairServiceManager
from src.services.inventory_service import InventoryManager
from src.services.quality_control import QualityControlManager

class CommandLineInterface:
    def __init__(self, repair_company):
        self.repair_company = repair_company

    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("REPAIR COMPANY MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Client Management")
            print("2. Repair Orders")
            print("3. Inventory Management")
            print("4. Employee Management")
            print("5. Financial Operations")
            print("6. Reports and Analytics")
            print("7. Quality Control")
            print("8. Interactive Demo Mode")
            print("0. Exit")
            
            choice = InputHandler.get_integer_input("Select option", 0, 8)
            
            if choice == 0:
                print("Thank you for using Repair Company System!")
                break
            elif choice == 1:
                self.client_management_menu()
            elif choice == 2:
                self.repair_orders_menu()
            elif choice == 3:
                self.inventory_management_menu()
            elif choice == 4:
                self.employee_management_menu()
            elif choice == 5:
                self.financial_operations_menu()
            elif choice == 6:
                self.reports_menu()
            elif choice == 7:
                self.quality_control_menu()
            elif choice == 8:
                self.interactive_demo_mode()

    def client_management_menu(self):
        while True:
            print("\n" + "-"*30)
            print("CLIENT MANAGEMENT")
            print("-"*30)
            print("1. Register New Client")
            print("2. View All Clients")
            print("3. Find Client by ID")
            print("4. Update Client Information")
            print("5. Client Financial Operations")
            print("6. View Client Repair History")
            print("0. Back to Main Menu")
            
            choice = InputHandler.get_integer_input("Select option", 0, 6)
            
            if choice == 0:
                break
            elif choice == 1:
                self.register_new_client()
            elif choice == 2:
                self.view_all_clients()
            elif choice == 3:
                self.find_client_by_id()
            elif choice == 4:
                self.update_client_info()
            elif choice == 5:
                self.client_financial_operations()
            elif choice == 6:
                self.view_client_repair_history()

    def register_new_client(self):
        print("\n--- REGISTER NEW CLIENT ---")
        
        client_id = InputHandler.get_string_input("Enter Client ID", 1, 20)
        name = InputHandler.get_string_input("Enter full name", 2, 100)
        email = InputHandler.get_email_input("Enter email")
        phone = InputHandler.get_phone_input("Enter phone number")
        
        print("\n--- CLIENT ADDRESS ---")
        street = InputHandler.get_string_input("Enter street", 5, 100)
        city = InputHandler.get_string_input("Enter city", 2, 50)
        state = InputHandler.get_string_input("Enter state", 2, 50)
        zip_code = InputHandler.get_string_input("Enter ZIP code", 3, 10)
        country = InputHandler.get_string_input("Enter country", 2, 50)
        building = InputHandler.get_string_input("Enter building number", 1, 10)
        
        initial_balance = InputHandler.get_float_input("Enter initial balance", 0, 100000)
        
        try:
            address = Address(street, city, state, zip_code, country, building)
            client = Client(client_id, name, email, phone, address, initial_balance)
            self.repair_company.clients.append(client)
            
            print(f"\n✅ Client {name} registered successfully!")
            print(f"Client ID: {client_id}")
            print(f"Initial Balance: ${initial_balance:.2f}")
            print(f"Loyalty Tier: {client.calculate_loyalty_tier()}")
            
        except Exception as e:
            print(f"❌ Error registering client: {e}")

    def view_all_clients(self):
        print("\n--- ALL REGISTERED CLIENTS ---")
        
        if not self.repair_company.clients:
            print("No clients registered.")
            return
            
        for i, client in enumerate(self.repair_company.clients, 1):
            repair_count = len(client.repair_history)
            print(f"{i}. {client.name} ({client.client_id}) - Balance: ${client.balance:.2f} - Repairs: {repair_count} - Tier: {client.calculate_loyalty_tier()}")

    def find_client_by_id(self):
        client_id = InputHandler.get_string_input("Enter Client ID to search")
        
        found_client = None
        for client in self.repair_company.clients:
            if client.client_id == client_id:
                found_client = client
                break
                
        if found_client:
            self.display_client_details(found_client)
        else:
            print(f"❌ Client with ID {client_id} not found.")

    def display_client_details(self, client):
        print("\n" + "="*50)
        print("CLIENT DETAILS")
        print("="*50)
        print(f"ID: {client.client_id}")
        print(f"Name: {client.name}")
        print(f"Email: {client.email}")
        print(f"Phone: {client.phone}")
        print(f"Address: {client.address.get_full_address()}")
        print(f"Balance: ${client.balance:.2f}")
        print(f"Loyalty Points: {client.loyalty_points}")
        print(f"Loyalty Tier: {client.calculate_loyalty_tier()}")
        print(f"Repair History: {len(client.repair_history)} orders")
        print(f"Discount Percentage: {client.calculate_discount()}%")

    def update_client_info(self):
        client_id = InputHandler.get_string_input("Enter Client ID to update")
        
        client = None
        for c in self.repair_company.clients:
            if c.client_id == client_id:
                client = c
                break
                
        if not client:
            print(f"❌ Client with ID {client_id} not found.")
            return
            
        print(f"\nUpdating client: {client.name}")
        print("1. Update Email")
        print("2. Update Phone")
        print("3. Update Address")
        print("4. Add Funds")
        print("5. Add Loyalty Points")
        
        choice = InputHandler.get_integer_input("Select field to update", 1, 5)
        
        if choice == 1:
            new_email = InputHandler.get_email_input("Enter new email")
            client.email = new_email
            print("✅ Email updated successfully!")
            
        elif choice == 2:
            new_phone = InputHandler.get_phone_input("Enter new phone")
            client.phone = new_phone
            print("✅ Phone updated successfully!")
            
        elif choice == 3:
            self.update_client_address(client)
            
        elif choice == 4:
            amount = InputHandler.get_float_input("Enter amount to add", 1, 10000)
            client.add_funds(amount)
            print(f"✅ ${amount:.2f} added to client balance!")
            print(f"New balance: ${client.balance:.2f}")
            
        elif choice == 5:
            points = InputHandler.get_integer_input("Enter loyalty points to add", 1, 1000)
            client.add_loyalty_points(points)
            print(f"✅ {points} loyalty points added!")
            print(f"New loyalty tier: {client.calculate_loyalty_tier()}")

    def update_client_address(self, client):
        print("\n--- UPDATE ADDRESS ---")
        street = InputHandler.get_string_input("Enter street", 5, 100)
        city = InputHandler.get_string_input("Enter city", 2, 50)
        state = InputHandler.get_string_input("Enter state", 2, 50)
        zip_code = InputHandler.get_string_input("Enter ZIP code", 3, 10)
        country = InputHandler.get_string_input("Enter country", 2, 50)
        building = InputHandler.get_string_input("Enter building number", 1, 10)
        
        client.address = Address(street, city, state, zip_code, country, building)
        print("✅ Address updated successfully!")

    def client_financial_operations(self):
        client_id = InputHandler.get_string_input("Enter Client ID")
        
        client = None
        for c in self.repair_company.clients:
            if c.client_id == client_id:
                client = c
                break
                
        if not client:
            print(f"❌ Client with ID {client_id} not found.")
            return
            
        print(f"\nFinancial Operations for: {client.name}")
        print("1. Check Balance")
        print("2. Add Funds")
        print("3. Transfer to Another Client")
        print("4. View Transaction History")
        
        choice = InputHandler.get_integer_input("Select operation", 1, 4)
        
        if choice == 1:
            print(f"Current Balance: ${client.balance:.2f}")
            print(f"Loyalty Points: {client.loyalty_points}")
            print(f"Available Discount: {client.calculate_discount()}%")
            
        elif choice == 2:
            amount = InputHandler.get_float_input("Enter amount to add", 1, 10000)
            client.add_funds(amount)
            print(f"✅ ${amount:.2f} added. New balance: ${client.balance:.2f}")
            
        elif choice == 3:
            target_id = InputHandler.get_string_input("Enter target Client ID")
            target_client = None
            for c in self.repair_company.clients:
                if c.client_id == target_id:
                    target_client = c
                    break
                    
            if not target_client:
                print(f"❌ Target client with ID {target_id} not found.")
                return
                
            amount = InputHandler.get_float_input("Enter transfer amount", 1, client.balance)
            
            if client.transfer_to_another_client(target_client, amount):
                print(f"✅ Transfer successful! ${amount:.2f} sent to {target_client.name}")
                print(f"Your new balance: ${client.balance:.2f}")
            else:
                print("❌ Transfer failed.")

    def view_client_repair_history(self):
        client_id = InputHandler.get_string_input("Enter Client ID")
        
        client = None
        for c in self.repair_company.clients:
            if c.client_id == client_id:
                client = c
                break
                
        if not client:
            print(f"❌ Client with ID {client_id} not found.")
            return
            
        print(f"\nRepair History for: {client.name}")
        print("-" * 40)
        
        if not client.repair_history:
            print("No repair history found.")
            return
            
        for i, order in enumerate(client.repair_history, 1):
            status_icon = "✅" if order.status == "COMPLETED" else "🔄"
            print(f"{i}. {status_icon} Order {order.order_id} - {order.device_description}")
            print(f"   Problem: {order.problem_description}")
            print(f"   Status: {order.status} - Cost: ${order.total_cost:.2f}")
            if order.completion_date:
                print(f"   Completed: {order.completion_date}")
            print()

    def repair_orders_menu(self):
        while True:
            print("\n" + "-"*30)
            print("REPAIR ORDERS MANAGEMENT")
            print("-"*30)
            print("1. Create New Repair Order")
            print("2. View All Orders")
            print("3. Find Order by ID")
            print("4. Update Order Status")
            print("5. Assign Technician")
            print("6. Complete Repair Order")
            print("7. Add Parts to Order")
            print("0. Back to Main Menu")
            
            choice = InputHandler.get_integer_input("Select option", 0, 7)
            
            if choice == 0:
                break
            elif choice == 1:
                self.create_repair_order()
            elif choice == 2:
                self.view_all_orders()
            elif choice == 3:
                self.find_order_by_id()
            elif choice == 4:
                self.update_order_status()
            elif choice == 5:
                self.assign_technician()
            elif choice == 6:
                self.complete_repair_order()
            elif choice == 7:
                self.add_parts_to_order()

    def create_repair_order(self):
        print("\n--- CREATE NEW REPAIR ORDER ---")
        
        if not self.repair_company.clients:
            print("❌ No clients registered. Please register a client first.")
            return
            
        print("Select client:")
        for i, client in enumerate(self.repair_company.clients, 1):
            print(f"{i}. {client.name} ({client.client_id})")
            
        client_choice = InputHandler.get_integer_input("Enter client number", 1, len(self.repair_company.clients))
        client = self.repair_company.clients[client_choice - 1]
        
        order_id = InputHandler.get_string_input("Enter Order ID", 1, 20)
        device_desc = InputHandler.get_string_input("Enter device description", 5, 200)
        problem_desc = InputHandler.get_string_input("Enter problem description", 10, 500)
        
        priorities = ["LOW", "NORMAL", "HIGH", "URGENT"]
        priority = InputHandler.get_choice_input("Select priority level", priorities)
        
        if not self.repair_company.repair_service_manager.repair_services:
            print("❌ No services available. Creating default service.")
            service = RepairService("SRV001", "General Repair", "Standard repair service", 
                                  100.0, 1.0, [], 5, 90)
        else:
            service = self.repair_company.repair_service_manager.repair_services[0]
        
        try:
            order = RepairOrder(order_id, client, device_desc, problem_desc, 
                              service, None, priority, "2024-01-01")
            
            self.repair_company.repair_service_manager.active_orders.append(order)
            client.repair_history.append(order)
            
            print(f"\n✅ Repair Order {order_id} created successfully!")
            print(f"Client: {client.name}")
            print(f"Device: {device_desc}")
            print(f"Priority: {priority}")
            print(f"Initial Status: {order.status}")
            
        except Exception as e:
            print(f"❌ Error creating repair order: {e}")

    def view_all_orders(self):
        manager = self.repair_company.repair_service_manager
        print("\n--- ACTIVE REPAIR ORDERS ---")
        
        if not manager.active_orders:
            print("No active orders.")
        else:
            for i, order in enumerate(manager.active_orders, 1):
                technician_name = order.technician_assigned.get_full_name() if order.technician_assigned else "Unassigned"
                print(f"{i}. 📋 Order {order.order_id}")
                print(f"   Client: {order.client.name}")
                print(f"   Device: {order.device_description}")
                print(f"   Status: {order.status} - Priority: {order.priority_level}")
                print(f"   Technician: {technician_name}")
                print()
        
        print("\n--- COMPLETED ORDERS ---")
        if not manager.completed_orders:
            print("No completed orders.")
        else:
            for i, order in enumerate(manager.completed_orders, 1):
                print(f"{i}. ✅ Order {order.order_id} - {order.device_description}")
                print(f"   Completed: {order.completion_date} - Cost: ${order.total_cost:.2f}")
                print()

    def find_order_by_id(self):
        order_id = InputHandler.get_string_input("Enter Order ID to search")
        
        manager = self.repair_company.repair_service_manager
        found_order = manager._find_order_by_id(order_id)
        
        if found_order:
            self.display_order_details(found_order)
        else:
            print(f"❌ Order with ID {order_id} not found.")

    def display_order_details(self, order):
        print("\n" + "="*50)
        print("REPAIR ORDER DETAILS")
        print("="*50)
        print(f"Order ID: {order.order_id}")
        print(f"Client: {order.client.name}")
        print(f"Device: {order.device_description}")
        print(f"Problem: {order.problem_description}")
        print(f"Service: {order.service_required.name}")
        print(f"Status: {order.status}")
        print(f"Priority: {order.priority_level}")
        print(f"Creation Date: {order.creation_date}")
        
        if order.technician_assigned:
            print(f"Technician: {order.technician_assigned.get_full_name()}")
        else:
            print("Technician: Not assigned")
            
        print(f"Actual Hours: {order.actual_hours}")
        print(f"Used Parts: {len(order.used_parts)}")
        print(f"Total Cost: ${order.total_cost:.2f}")
        
        if order.completion_date:
            print(f"Completion Date: {order.completion_date}")
        if order.warranty_expiry_date:
            print(f"Warranty Expiry: {order.warranty_expiry_date}")

    def update_order_status(self):
        order_id = InputHandler.get_string_input("Enter Order ID")
        
        manager = self.repair_company.repair_service_manager
        order = manager._find_order_by_id(order_id)
        
        if not order:
            print(f"❌ Order with ID {order_id} not found.")
            return
            
        print(f"Current status: {order.status}")
        status_options = ["CREATED", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
        new_status = InputHandler.get_choice_input("Select new status", status_options)
        
        if new_status == "IN_PROGRESS":
            order.mark_in_progress()
        elif new_status == "COMPLETED":
            actual_hours = InputHandler.get_float_input("Enter actual hours worked", 0.5, 100)
            order.mark_completed(actual_hours)
        
        print(f"✅ Order status updated to: {order.status}")

    def assign_technician(self):
        order_id = InputHandler.get_string_input("Enter Order ID")
        
        manager = self.repair_company.repair_service_manager
        order = manager._find_order_by_id(order_id)
        
        if not order:
            print(f"❌ Order with ID {order_id} not found.")
            return
            
        if not self.repair_company.employees:
            print("❌ No technicians available.")
            return
            
        print("Available technicians:")
        technicians = [emp for emp in self.repair_company.employees if isinstance(emp, Technician)]
        
        for i, tech in enumerate(technicians, 1):
            availability = "✅ Available" if tech.is_available else "❌ Busy"
            print(f"{i}. {tech.get_full_name()} - Skill: {tech.skill_level}/10 - {availability}")
            
        tech_choice = InputHandler.get_integer_input("Select technician", 1, len(technicians))
        technician = technicians[tech_choice - 1]
        
        try:
            manager.assign_technician_to_order(order_id, technician)
            print(f"✅ Technician {technician.get_full_name()} assigned to order {order_id}")
        except Exception as e:
            print(f"❌ Error assigning technician: {e}")

    def complete_repair_order(self):
        order_id = InputHandler.get_string_input("Enter Order ID to complete")
        
        manager = self.repair_company.repair_service_manager
        order = manager._find_order_by_id(order_id)
        
        if not order:
            print(f"❌ Order with ID {order_id} not found.")
            return
            
        actual_hours = InputHandler.get_float_input("Enter actual hours worked", 0.5, 100)
        
        used_parts = []
        add_more_parts = True
        while add_more_parts and self.repair_company.inventory_manager.inventory_items:
            print("\nAvailable parts:")
            for i, item in enumerate(self.repair_company.inventory_manager.inventory_items, 1):
                print(f"{i}. {item.name} - Stock: {item.quantity_in_stock} - Price: ${item.price:.2f}")
                
            part_choice = InputHandler.get_integer_input("Select part (0 to skip)", 0, len(self.repair_company.inventory_manager.inventory_items))
            
            if part_choice == 0:
                add_more_parts = False
            else:
                part = self.repair_company.inventory_manager.inventory_items[part_choice - 1]
                quantity = InputHandler.get_integer_input(f"Enter quantity for {part.name}", 1, part.quantity_in_stock)
                used_parts.append({'part': part, 'quantity': quantity})
                
                add_more = InputHandler.get_yes_no_input("Add another part?")
                if not add_more:
                    add_more_parts = False
        
        try:
            total_cost = manager.complete_repair_order(order_id, actual_hours, used_parts)
            print(f"✅ Repair order {order_id} completed successfully!")
            print(f"Total cost: ${total_cost:.2f}")
            print(f"Client balance: ${order.client.balance:.2f}")
            
        except Exception as e:
            print(f"❌ Error completing repair order: {e}")

    def add_parts_to_order(self):
        order_id = InputHandler.get_string_input("Enter Order ID")
        
        manager = self.repair_company.repair_service_manager
        order = manager._find_order_by_id(order_id)
        
        if not order:
            print(f"❌ Order with ID {order_id} not found.")
            return
            
        if not self.repair_company.inventory_manager.inventory_items:
            print("❌ No inventory items available.")
            return
            
        print("Available parts:")
        for i, item in enumerate(self.repair_company.inventory_manager.inventory_items, 1):
            print(f"{i}. {item.name} - Stock: {item.quantity_in_stock} - Price: ${item.price:.2f}")
            
        part_choice = InputHandler.get_integer_input("Select part", 1, len(self.repair_company.inventory_manager.inventory_items))
        part = self.repair_company.inventory_manager.inventory_items[part_choice - 1]
        
        quantity = InputHandler.get_integer_input("Enter quantity", 1, part.quantity_in_stock)
        
        try:
            order.add_used_part(part, quantity)
            print(f"✅ Added {quantity} x {part.name} to order {order_id}")
            print(f"Part stock remaining: {part.quantity_in_stock}")
            
        except Exception as e:
            print(f"❌ Error adding part: {e}")

    # Остальные меню будут реализованы аналогично...

    def inventory_management_menu(self):
        print("\n📦 Inventory Management Menu")
        print("1. Add New Inventory Item")
        print("2. View All Inventory")
        print("3. Check Stock Levels")
        print("4. Restock Items")
        print("5. Generate Inventory Report")
        print("0. Back to Main Menu")
        
        choice = InputHandler.get_integer_input("Select option", 0, 5)
        
        if choice == 1:
            self.add_inventory_item()
        elif choice == 2:
            self.view_all_inventory()
        # Остальные опции...

    def add_inventory_item(self):
        print("\n--- ADD NEW INVENTORY ITEM ---")
        
        part_id = InputHandler.get_string_input("Enter Part ID", 1, 20)
        name = InputHandler.get_string_input("Enter part name", 2, 100)
        description = InputHandler.get_string_input("Enter description", 5, 200)
        category = InputHandler.get_string_input("Enter category", 2, 50)
        price = InputHandler.get_float_input("Enter price", 0.01, 10000)
        quantity = InputHandler.get_integer_input("Enter initial quantity", 0, 10000)
        min_stock = InputHandler.get_integer_input("Enter minimum stock level", 0, 1000)
        supplier = InputHandler.get_string_input("Enter supplier info", 2, 100)
        
        compatibilities = []
        print("Enter compatible devices (enter 'done' when finished):")
        while True:
            device = InputHandler.get_string_input("Device name (or 'done')")
            if device.lower() == 'done':
                break
            compatibilities.append(device)
        
        try:
            item = InventoryItem(part_id, name, description, category, price, 
                               quantity, min_stock, supplier, compatibilities)
            
            self.repair_company.inventory_manager.inventory_items.append(item)
            
            print(f"\n✅ Inventory item {name} added successfully!")
            print(f"Part ID: {part_id}")
            print(f"Initial Stock: {quantity}")
            print(f"Total Value: ${item.calculate_total_value():.2f}")
            
        except Exception as e:
            print(f"❌ Error adding inventory item: {e}")

    def view_all_inventory(self):
        print("\n--- INVENTORY ITEMS ---")
        
        if not self.repair_company.inventory_manager.inventory_items:
            print("No inventory items.")
            return
            
        total_value = 0
        for i, item in enumerate(self.repair_company.inventory_manager.inventory_items, 1):
            stock_status = "🟢" if not item.needs_restocking() else "🔴"
            print(f"{i}. {stock_status} {item.name} ({item.part_id})")
            print(f"   Category: {item.category} - Price: ${item.price:.2f}")
            print(f"   Stock: {item.quantity_in_stock} (Min: {item.min_stock_level})")
            print(f"   Value: ${item.calculate_total_value():.2f}")
            print()
            total_value += item.calculate_total_value()
        
        print(f"Total Inventory Value: ${total_value:.2f}")

    def employee_management_menu(self):
        print("\n👨‍💼 Employee Management - Under Construction")
        # Реализация управления сотрудниками

    def financial_operations_menu(self):
        print("\n💰 Financial Operations - Under Construction")
        # Реализация финансовых операций

    def reports_menu(self):
        print("\n📊 Reports and Analytics - Under Construction")
        # Реализация отчетов

    def quality_control_menu(self):
        print("\n🔍 Quality Control - Under Construction")
        # Реализация контроля качества

    def interactive_demo_mode(self):
        print("\n" + "="*60)
        print("🎮 INTERACTIVE DEMO MODE")
        print("="*60)
        print("Experience the full functionality with guided examples!")
        
        while True:
            print("\nDemo Options:")
            print("1. Quick Client Registration")
            print("2. Create Repair Order")
            print("3. Process Payment")
            print("4. Bank Transfer Demo")
            print("5. Inventory Management Demo")
            print("6. Complete Workflow Demo")
            print("0. Exit Demo")
            
            choice = InputHandler.get_integer_input("Select demo option", 0, 6)
            
            if choice == 0:
                break
            elif choice == 1:
                self.demo_client_registration()
            elif choice == 2:
                self.demo_repair_order()
            elif choice == 3:
                self.demo_payment_processing()
            elif choice == 4:
                self.demo_bank_transfer()
            elif choice == 5:
                self.demo_inventory_management()
            elif choice == 6:
                self.demo_complete_workflow()

    def demo_client_registration(self):
        print("\n--- CLIENT REGISTRATION DEMO ---")
        
        client_id = InputHandler.get_string_input("Enter demo Client ID (e.g., CL1001)")
        name = InputHandler.get_string_input("Enter client name")
        email = InputHandler.get_email_input("Enter email")
        phone = InputHandler.get_phone_input("Enter phone")
        
        address = Address("123 Demo Street", "Demo City", "DS", "12345", "Demo Country", "1A")
        client = Client(client_id, name, email, phone, address, 1000.0)
        
        self.repair_company.clients.append(client)
        print(f"✅ Demo client {name} created with $1000.00 balance!")
        print(f"Loyalty Tier: {client.calculate_loyalty_tier()}")

    def demo_repair_order(self):
        if not self.repair_company.clients:
            print("❌ No clients available. Please create a client first.")
            return
            
        client = self.repair_company.clients[0]
        
        order_id = InputHandler.get_string_input("Enter demo Order ID (e.g., RO2001)")
        device = InputHandler.get_string_input("Enter device description")
        problem = InputHandler.get_string_input("Enter problem description")
        
        service = RepairService("DEMO001", "Demo Repair", "Demo service", 150.0, 1.5, [], 5, 90)
        order = RepairOrder(order_id, client, device, problem, service, None, "NORMAL", "2024-01-01")
        
        self.repair_company.repair_service_manager.active_orders.append(order)
        client.repair_history.append(order)
        print(f"✅ Demo repair order {order_id} created!")
        print(f"Added to {client.name}'s repair history")

    def demo_payment_processing(self):
        if not self.repair_company.clients:
            print("❌ No clients available.")
            return
            
        client = self.repair_company.clients[0]
        amount = InputHandler.get_float_input("Enter payment amount", 1, client.balance)
        
        payment = Payment("PAY001", client, None, amount, "CASH", "2024-01-01")
        try:
            payment.process_payment()
            print(f"✅ Payment of ${amount:.2f} processed successfully!")
            print(f"Remaining balance: ${client.balance:.2f}")
            
            receipt = payment.generate_receipt()
            print("\n📄 Payment Receipt:")
            print(receipt)
            
        except Exception as e:
            print(f"❌ Payment failed: {e}")

    def demo_bank_transfer(self):
        if len(self.repair_company.clients) < 2:
            print("❌ Need at least 2 clients for transfer demo.")
            return
            
        client1 = self.repair_company.clients[0]
        client2 = self.repair_company.clients[1]
        
        account1 = BankAccount("ACC001", client1, "Bank", client1.balance, "USD")
        account2 = BankAccount("ACC002", client2, "Bank", client2.balance, "USD")
        
        print(f"💰 Current balances:")
        print(f"{client1.name}: ${account1.balance:.2f}")
        print(f"{client2.name}: ${account2.balance:.2f}")
        
        amount = InputHandler.get_float_input("Enter transfer amount", 1, account1.balance)
        
        try:
            account1.transfer_to_another_account(account2, amount)
            print(f"✅ Transfer of ${amount:.2f} successful!")
            print(f"New balances:")
            print(f"{client1.name}: ${account1.balance:.2f}")
            print(f"{client2.name}: ${account2.balance:.2f}")
            
            stats = account1.get_transaction_statistics()
            print(f"📊 Transaction stats: {stats['count']} transactions")
            
        except Exception as e:
            print(f"❌ Transfer failed: {e}")

    def demo_inventory_management(self):
        print("\n--- INVENTORY MANAGEMENT DEMO ---")
        
        part_id = InputHandler.get_string_input("Enter demo Part ID (e.g., PART999)")
        name = InputHandler.get_string_input("Enter part name")
        price = InputHandler.get_float_input("Enter price", 1, 1000)
        quantity = InputHandler.get_integer_input("Enter quantity", 1, 1000)
        
        item = InventoryItem(part_id, name, "Demo part", "Demo Category", price, quantity, 5, "Demo Supplier", [])
        self.repair_company.inventory_manager.inventory_items.append(item)
        
        print(f"✅ Demo inventory item {name} created!")
        print(f"Stock: {quantity} - Value: ${item.calculate_total_value():.2f}")
        
        # Demonstrate restocking
        if quantity < 10:
            restock_qty = 20 - quantity
            item.restock_items(restock_qty)
            print(f"🔄 Restocked {restock_qty} units. New stock: {item.quantity_in_stock}")

    def demo_complete_workflow(self):
        print("\n--- COMPLETE WORKFLOW DEMO ---")
        print("This demo shows a complete repair workflow from start to finish!")
        
        # Create client
        address = Address("456 Workflow Ave", "Demo City", "DC", "54321", "Demo Country", "10B")
        client = Client("WF001", "Workflow User", "workflow@demo.com", "+1555123456", address, 2000.0)
        self.repair_company.clients.append(client)
        print("✅ Step 1: Client created")
        
        # Create technician
        tech = Technician("TWF001", "Workflow", "Tech", "Technician", 50000.0, 
                         "2024-01-01", "Repair", address, "Electronics", 8, [])
        self.repair_company.employees.append(tech)
        self.repair_company.repair_service_manager.available_technicians.append(tech)
        print("✅ Step 2: Technician created")
        
        # Create service
        service = RepairService("SWF001", "Workflow Service", "Complete workflow service", 
                              200.0, 2.0, [], 6, 120)
        self.repair_company.repair_service_manager.repair_services.append(service)
        print("✅ Step 3: Service created")
        
        # Create inventory item
        inventory_item = InventoryItem("PWF001", "Workflow Part", "Demo part for workflow", 
                                     "Components", 75.0, 50, 10, "Workflow Supplier", [])
        self.repair_company.inventory_manager.inventory_items.append(inventory_item)
        print("✅ Step 4: Inventory item created")
        
        # Create repair order
        order = RepairOrder("OWF001", client, "Workflow Device", "Complete workflow test", 
                          service, None, "HIGH", "2024-01-01")
        self.repair_company.repair_service_manager.active_orders.append(order)
        client.repair_history.append(order)
        print("✅ Step 5: Repair order created")
        
        # Assign technician
        try:
            self.repair_company.repair_service_manager.assign_technician_to_order("OWF001", tech)
            print("✅ Step 6: Technician assigned")
        except Exception as e:
            print(f"❌ Step 6 failed: {e}")
        
        # Add parts
        try:
            order.add_used_part(inventory_item, 2)
            print("✅ Step 7: Parts added to order")
        except Exception as e:
            print(f"❌ Step 7 failed: {e}")
        
        # Complete order
        try:
            order.mark_completed(2.5)
            total_cost = order.calculate_total_cost()
            print(f"✅ Step 8: Order completed - Total cost: ${total_cost:.2f}")
        except Exception as e:
            print(f"❌ Step 8 failed: {e}")
        
        # Process payment
        try:
            payment = Payment("PWF001", client, order, total_cost, "CREDIT_CARD", "2024-01-02")
            payment.process_payment()
            print(f"✅ Step 9: Payment processed - Remaining balance: ${client.balance:.2f}")
        except Exception as e:
            print(f"❌ Step 9 failed: {e}")
        
        print("\n🎉 WORKFLOW DEMO COMPLETED SUCCESSFULLY!")
        print("All steps completed from client registration to payment processing.")