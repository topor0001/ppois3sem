from src.ui.command_line_interface import CommandLineInterface
from src.services.repair_service import RepairServiceManager
from src.services.inventory_service import InventoryManager
from src.services.quality_control import QualityControlManager
from src.ui.input_handler import get_integer_input  # Импортируем функцию напрямую

class InteractiveRepairCompany:
    def __init__(self):
        self.clients = []
        self.employees = []
        self.repair_service_manager = RepairServiceManager()
        self.inventory_manager = InventoryManager()
        self.quality_control_manager = QualityControlManager()
        self.cli = CommandLineInterface(self)

    def run_interactive_system(self):
        print("🚀 Starting Repair Company Interactive System...")
        print("Version 1.0 - Complete Management System")
        
        self.load_demo_data()
        
        print("\nChoose mode:")
        print("1. Full Interactive Mode")
        print("2. Demo Mode")
        print("3. Exit")
        
        # Используем функцию напрямую
        choice = get_integer_input("Select mode", 1, 3)
        
        if choice == 1:
            self.cli.main_menu()
        elif choice == 2:
            self.cli.interactive_demo_mode()
        else:
            print("Goodbye!")

    def load_demo_data(self):
        try:
            # Проверьте, существуют ли эти файлы!
            from src.models.address import Address
            from src.models.client import Client
            from src.models.technician import Technician
            from src.models.service import RepairService
            from src.models.inventory import InventoryItem
            
            # ... остальной код загрузки данных
            
        except ImportError as e:
            print(f"❌ Ошибка импорта: {e}")
            print("   Проверьте, что все файлы существуют:")
            print("   - src/models/address.py")
            print("   - src/models/client.py")
            print("   - src/models/technician.py")
            print("   - src/models/service.py")
            print("   - src/models/inventory.py")
        except Exception as e:
            print(f"❌ Ошибка загрузки демо-данных: {e}")

if __name__ == "__main__":
    company = InteractiveRepairCompany()
    company.run_interactive_system()