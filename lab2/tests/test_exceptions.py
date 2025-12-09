import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.exceptions.appointment_conflict_exception import AppointmentConflictException
from src.exceptions.invalid_order_data_exception import InvalidOrderDataException
from src.exceptions.invalid_part_data_exception import InvalidPartDataException
from src.exceptions.order_not_found_exception import OrderNotFoundException
from src.exceptions.repair_quality_exception import RepairQualityException
from src.exceptions.technician_not_available_exception import TechnicianNotAvailableException
from src.exceptions.warranty_expired_exception import WarrantyExpiredException

class TestExceptions(unittest.TestCase):
    def test_appointment_conflict_exception(self):
        exc = AppointmentConflictException("T001", "2024-01-15")
        self.assertEqual(exc.error_code, "APPOINTMENT_CONFLICT")
        self.assertIn("Appointment conflict", str(exc))
    
    def test_invalid_order_data_exception(self):
        exc = InvalidOrderDataException("order_id", "")
        self.assertEqual(exc.error_code, "INVALID_ORDER_DATA")
        self.assertIn("Invalid order data", str(exc))
    
    def test_invalid_part_data_exception(self):
        exc = InvalidPartDataException("price", -10.0)
        self.assertEqual(exc.error_code, "INVALID_PART_DATA")
        self.assertIn("Invalid part data", str(exc))
    
    def test_order_not_found_exception(self):
        exc = OrderNotFoundException("RO999")
        self.assertEqual(exc.error_code, "ORDER_NOT_FOUND")
        self.assertIn("Order with ID RO999", str(exc))
    
    def test_repair_quality_exception(self):
        exc = RepairQualityException("RO001", "Poor soldering")
        self.assertEqual(exc.error_code, "REPAIR_QUALITY_ISSUE")
        self.assertIn("Repair quality issue", str(exc))
    
    def test_technician_not_available_exception(self):
        exc = TechnicianNotAvailableException("T001")
        self.assertEqual(exc.error_code, "TECHNICIAN_NOT_AVAILABLE")
        self.assertIn("Technician with ID T001", str(exc))
    
    def test_warranty_expired_exception(self):
        exc = WarrantyExpiredException("RO001", "2024-01-01")
        self.assertEqual(exc.error_code, "WARRANTY_EXPIRED")
        self.assertIn("Warranty for order RO001", str(exc))

if __name__ == '__main__':
    unittest.main()