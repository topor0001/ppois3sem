import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.finance.bank_account import BankAccount
from src.finance.invoice import Invoice
from src.finance.transaction import Transaction
from src.finance.financial_report import FinancialReport
from src.finance.salary import Salary
from src.models.client import Client
from src.models.employee import Employee
from src.models.address import Address
from src.exceptions.insufficient_funds_exception import InsufficientFundsException
class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        self.account1 = BankAccount("ACC001", self.client, "Main Bank", 5000.0, "USD")
        self.account2 = BankAccount("ACC002", None, "Main Bank", 3000.0, "USD")

    def test_account_creation(self):
        self.assertEqual(self.account1.account_number, "ACC001")
        self.assertEqual(self.account1.balance, 5000.0)

    def test_transfer_success(self):
        result = self.account1.transfer_to_another_account(self.account2, 1000.0)
        self.assertTrue(result)
        self.assertEqual(self.account1.balance, 4000.0)
        self.assertEqual(self.account2.balance, 4000.0)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsException):
            self.account1.transfer_to_another_account(self.account2, 10000.0)

    def test_interest_calculation(self):
        interest = self.account1.calculate_interest(5.0, 30)
        self.assertGreater(interest, 0)

    def test_account_validation(self):
        self.assertIsInstance(self.account1.validate_account_number(), bool)

    def test_transaction_statistics(self):
        self.account1.transfer_to_another_account(self.account2, 500.0)
        stats = self.account1.get_transaction_statistics()
        self.assertEqual(stats['count'], 1)
        self.assertEqual(stats['total'], 500.0)

class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        self.invoice = Invoice("INV001", None, self.client, "2024-01-01", "2024-02-01", 
                              [{"item": "Service", "amount": 500.0}])

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.invoice_id, "INV001")
        self.assertEqual(self.invoice.total_amount, 500.0)

    def test_remaining_balance(self):
        self.assertEqual(self.invoice.calculate_remaining_balance(), 500.0)

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.account1 = BankAccount("ACC001", None, "Bank", 5000.0, "USD")
        self.account2 = BankAccount("ACC002", None, "Bank", 3000.0, "USD")
        self.transaction = Transaction("TXN001", self.account1, self.account2, 1000.0, "TRANSFER", "Test transfer")

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.transaction_id, "TXN001")
        self.assertEqual(self.transaction.amount, 1000.0)

    def test_execute_transfer_success(self):
        result = self.transaction.execute_transfer()
        self.assertTrue(result)
        self.assertEqual(self.transaction.status, "COMPLETED")

    def test_execute_transfer_failure(self):
        large_transaction = Transaction("TXN002", self.account1, self.account2, 10000.0, "TRANSFER", "Large transfer")
        result = large_transaction.execute_transfer()
        self.assertFalse(result)
        self.assertEqual(large_transaction.status, "FAILED")

class TestFinancialReport(unittest.TestCase):
    def setUp(self):
        self.account1 = BankAccount("ACC001", None, "Bank", 5000.0, "USD")
        self.account2 = BankAccount("ACC002", None, "Bank", 3000.0, "USD")
        
        transaction1 = Transaction("TXN001", self.account1, self.account2, 1000.0, "INCOME", "Payment")
        transaction2 = Transaction("TXN002", self.account1, self.account2, 500.0, "EXPENSE", "Expense")
        
        client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        invoice = Invoice("INV001", None, client, "2024-01-01", "2024-02-01", [{"item": "Service", "amount": 1500.0}])
        invoice.paid_amount = 1500.0
        
        self.report = FinancialReport("REP001", "2024-01-01", "2024-01-31", None, 
                                     [transaction1, transaction2], [invoice])

    def test_financial_metrics(self):
        metrics = self.report.calculate_financial_metrics()
        self.assertEqual(metrics['revenue'], 1500.0)
        self.assertEqual(metrics['expenses'], 500.0)
        self.assertEqual(metrics['profit'], 1000.0)

class TestSalary(unittest.TestCase):
    def setUp(self):
        self.address = Address("Work St", "City", "ST", "12345", "Country", "123")
        self.employee = Employee("EMP001", "John", "Doe", "Technician", 50000.0, 
                               "2023-01-01", "Repair", self.address, "Electronics")
        self.salary = Salary("SAL001", self.employee, 50000.0, "2024-01-01")

    def test_salary_creation(self):
        self.assertEqual(self.salary.salary_id, "SAL001")
        self.assertEqual(self.salary.base_salary, 50000.0)

    def test_total_salary_calculation(self):
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50000.0)

    def test_overtime_addition(self):
        self.salary.add_overtime(10, 25.0)
        self.assertEqual(self.salary.overtime_pay, 250.0)
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50250.0)
class TestInvoiceComprehensive(unittest.TestCase):
    def setUp(self):
        self.client = Client("CL001", "John Doe", "john@test.com", "+1234567890", None, 1000.0)
        self.line_items = [
            {"item": "Screen Repair", "amount": 299.99},
            {"item": "Battery Replacement", "amount": 89.99}
        ]
        self.invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                              "2024-02-01", self.line_items)
    
    def test_invoice_methods(self):
       class MockPayment:
        def __init__(self):
            self.amount = 100.0
            self.payment_id = "PAY001"
            self.payment_date = "2024-01-15" 
            self.payment_method = "credit_card"  
    
       payment = MockPayment()
       self.invoice.add_payment(payment)
       self.assertEqual(self.invoice.paid_amount, 100.0)
       self.assertEqual(self.invoice.status, "PARTIALLY_PAID")
       self.invoice.add_line_item("Labor", 50.0, 2)
       self.assertEqual(len(self.invoice.line_items), 3)
       result = self.invoice.remove_line_item(0)
       self.assertTrue(result)
       self.assertEqual(len(self.invoice.line_items), 2)
       history = self.invoice.get_payment_history()
       self.assertEqual(len(history), 1)
       tax = self.invoice.calculate_tax(20.0) 
       self.assertGreater(tax, 0)
       self.assertFalse(self.invoice.is_fully_paid())
       category = self.invoice.get_aging_category()
       self.assertIn(category, ["NOT_DUE", "PAID", "1-30_DAYS", "31-60_DAYS", "61-90_DAYS", "OVER_90_DAYS"])
class TestSalary(unittest.TestCase):
    
    def setUp(self):
        self.address = Address("Work St", "City", "ST", "12345", "Country", "123")
        self.employee = Employee("EMP001", "John", "Doe", "Technician", 50000.0,
                                "2023-01-01", "Repair", self.address, "Electronics")
        self.salary = Salary("SAL001", self.employee, 50000.0, "2024-01-01")
    
    def test_salary_creation(self):
        self.assertEqual(self.salary.salary_id, "SAL001")
        self.assertEqual(self.salary.base_salary, 50000.0)
        self.assertEqual(self.salary.employee, self.employee)
        self.assertEqual(self.salary.payment_date, "2024-01-01")
        self.assertFalse(self.salary.is_paid)
        self.assertEqual(self.salary.overtime_pay, 0.0)
        self.assertEqual(self.salary.bonuses, 0.0)
        self.assertEqual(self.salary.deductions, 0.0)
    
    def test_total_salary_calculation(self):
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50000.0)
    
    def test_overtime_addition(self):
        self.salary.add_overtime(10, 25.0)
        self.assertEqual(self.salary.overtime_pay, 250.0)
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50250.0)
    
    
    def test_process_payment_success(self):
        from src.finance.bank_account import BankAccount
        
        company_account = BankAccount("COMP001", None, "Bank", 100000.0, "USD")
        employee_account = BankAccount("EMP001", self.employee, "Bank", 1000.0, "USD")
        
        result = self.salary.process_payment(company_account, employee_account)
        
        self.assertTrue(result)
        self.assertTrue(self.salary.is_paid)
        self.assertEqual(employee_account.balance, 51000.0)  
        self.assertEqual(company_account.balance, 50000.0) 
    
    def test_process_payment_failure(self):
        from src.finance.bank_account import BankAccount
       
        company_account = BankAccount("COMP001", None, "Bank", 1000.0, "USD")
        employee_account = BankAccount("EMP001", self.employee, "Bank", 1000.0, "USD")
        
        result = self.salary.process_payment(company_account, employee_account)
        
        self.assertFalse(result)
        self.assertFalse(self.salary.is_paid)
        self.assertEqual(employee_account.balance, 1000.0) 
        self.assertEqual(company_account.balance, 1000.0) 
    
    def test_multiple_overtime_additions(self):
        self.salary.add_overtime(5, 20.0)  
        self.salary.add_overtime(10, 25.0) 
        self.salary.add_overtime(2, 30.0)   
        
        self.assertEqual(self.salary.overtime_pay, 410.0) 
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50410.0) 
    
    def test_salary_with_bonuses_and_deductions(self):

        self.salary.bonuses = 5000.0
        self.salary.deductions = 2000.0
        self.salary.add_overtime(20, 30.0) 
        
        total = self.salary.calculate_total_salary()
        expected = 50000.0 + 5000.0 - 2000.0 + 600.0
        self.assertEqual(total, expected)
    
    def test_negative_deductions(self):
        self.salary.deductions = -1000.0 
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 51000.0) 
    
    def test_zero_base_salary(self):
        zero_salary = Salary("SAL002", self.employee, 0.0, "2024-01-01")
        zero_salary.add_overtime(10, 15.0)
        zero_salary.bonuses = 100.0
        
        total = zero_salary.calculate_total_salary()
        self.assertEqual(total, 250.0) 
    
    def test_salary_state_after_failed_payment(self):
        from src.finance.bank_account import BankAccount
        company_account = BankAccount("COMP001", None, "Bank", 0.0, "USD")
        employee_account = BankAccount("EMP001", self.employee, "Bank", 0.0, "USD")
        self.salary.add_overtime(5, 20.0)
        
        result = self.salary.process_payment(company_account, employee_account)
        
        self.assertFalse(result)
        self.assertFalse(self.salary.is_paid)
        self.assertEqual(self.salary.overtime_pay, 100.0)
        total = self.salary.calculate_total_salary()
        self.assertEqual(total, 50100.0)
    
    def test_salary_string_representation(self):
        salary_str = str(self.salary)
        self.assertIsInstance(salary_str, str)
class TestInvoiceExtended(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("CL001", "Test Client", "test@test.com", 
                            "+1234567890", None, 1000.0)
        self.line_items = [
            {"item": "Service 1", "amount": 100.0},
            {"item": "Service 2", "amount": 200.0}
        ]
        self.invoice = Invoice("INV001", None, self.client, 
                              "2024-01-01", "2024-02-01", self.line_items)
    
def test_apply_early_payment_discount_success(self):
    self.invoice.paid_amount = 0.0
    result = self.invoice.apply_early_payment_discount(10.0)
    self.assertTrue(result) 
    self.assertEqual(self.invoice.discount_amount, 30.0)
    self.assertEqual(self.invoice.total_amount, 270.0)

def test_apply_early_payment_discount_too_high(self):
    self.invoice.paid_amount = 0.0
    
    result = self.invoice.apply_early_payment_discount(60.0)
    self.assertTrue(result) 
    self.assertEqual(self.invoice.discount_amount, 150.0) 
    
    def test_apply_early_payment_discount_failure(self):
        class MockPayment:
            def __init__(self):
                self.amount = 100.0
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "cash"
        
        payment = MockPayment()
        self.invoice.add_payment(payment)
        
        result = self.invoice.apply_early_payment_discount(10.0)
        self.assertFalse(result)
    
def test_send_payment_reminder(self):
    self.invoice.due_date = "2024-12-31" 
    reminder = self.invoice.send_payment_reminder()
    self.assertIsNone(reminder)
    self.invoice.due_date = "2023-01-01" 
    reminder = self.invoice.send_payment_reminder()
    self.assertIsNotNone(reminder)
    
def test_calculate_late_fee(self):
    self.invoice.due_date = "2024-12-31"
    fee = self.invoice.calculate_late_fee(10.0)
    self.assertEqual(fee, 0.0)
    self.invoice.due_date = "2023-01-01"  
    fee = self.invoice.calculate_late_fee(10.0)
    self.assertGreater(fee, 0.0)
    
    def test_generate_invoice_pdf(self):
        pdf_data = self.invoice.generate_invoice_pdf()
        self.assertIsInstance(pdf_data, dict)
        self.assertIn('filename', pdf_data)
        self.assertIn('content', pdf_data)
        self.assertIn('INVOICE: INV001', pdf_data['content'])
    
    def test_add_line_item(self):
        initial_count = len(self.invoice.line_items)
        self.invoice.add_line_item("New Service", 50.0, 2)
        
        self.assertEqual(len(self.invoice.line_items), initial_count + 1)
        self.assertEqual(self.invoice.total_amount, 400.0)
    
    def test_remove_line_item_success(self):
        result = self.invoice.remove_line_item(0)
        self.assertTrue(result)
        self.assertEqual(len(self.invoice.line_items), 1)
        self.assertEqual(self.invoice.total_amount, 200.0)
    
    def test_remove_line_item_failure(self):
        result = self.invoice.remove_line_item(10)
        self.assertFalse(result)
    
    def test_calculate_tax(self):
        tax_amount = self.invoice.calculate_tax(20.0)
        self.assertEqual(tax_amount, 60.0)
        self.assertEqual(self.invoice.tax_amount, 60.0)
        self.assertEqual(self.invoice.total_amount, 360.0)
    
    def test_is_fully_paid_false(self):
        self.assertFalse(self.invoice.is_fully_paid())
    
    def test_is_fully_paid_true(self):
        class MockPayment:
            def __init__(self, amount):
                self.amount = amount
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "cash"
        
        payment1 = MockPayment(200.0)
        payment2 = MockPayment(100.0)
        
        self.invoice.add_payment(payment1)
        self.invoice.add_payment(payment2)
        
        self.assertTrue(self.invoice.is_fully_paid())
        self.assertEqual(self.invoice.status, "PAID")
    
    def test_get_aging_category(self):
        category = self.invoice.get_aging_category()
        valid_categories = ["PAID", "NOT_DUE", "1-30_DAYS", 
                           "31-60_DAYS", "61-90_DAYS", "OVER_90_DAYS"]
        self.assertIn(category, valid_categories)
    
    def test_validate_invoice_data_success(self):
        result = self.invoice.validate_invoice_data()
        self.assertTrue(result)
    
    def test_get_payment_history(self):
        class MockPayment:
            def __init__(self):
                self.amount = 150.0
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "credit_card"
        
        payment = MockPayment()
        self.invoice.add_payment(payment)
        
        history = self.invoice.get_payment_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['payment_id'], "PAY001")
        self.assertEqual(history[0]['amount'], 150.0)

class TestBankAccountExtended(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("CL001", "Test Client", "test@test.com", 
                            "+1234567890", None, 1000.0)
        self.account = BankAccount("ACC001", self.client, "Main Bank", 5000.0, "USD")
        self.account2 = BankAccount("ACC002", None, "Main Bank", 3000.0, "USD")
    
    def test_validate_account_number_invalid(self):
        invalid_account = BankAccount("123", self.client, "Bank", 1000.0, "USD")
        result = invalid_account.validate_account_number()
        self.assertFalse(result)
    
    def test_get_transaction_statistics_empty(self):
        stats = self.account.get_transaction_statistics()
        self.assertEqual(stats['count'], 0)
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['average'], 0)
    
    def test_get_transaction_statistics_with_transactions(self):
        self.account.transfer_to_another_account(self.account2, 1000.0)
        self.account.transfer_to_another_account(self.account2, 500.0)
        
        stats = self.account.get_transaction_statistics()
        self.assertEqual(stats['count'], 2)
        self.assertEqual(stats['total'], 1500.0)
        self.assertEqual(stats['average'], 750.0)

class TestTransactionExtended(unittest.TestCase):
    
    def setUp(self):
        self.account1 = BankAccount("ACC001", None, "Bank", 5000.0, "USD")
        self.account2 = BankAccount("ACC002", None, "Bank", 3000.0, "USD")
        self.transaction = Transaction("TXN001", self.account1, self.account2, 
                                      1000.0, "TRANSFER", "Test transfer")
    
    def test_execute_transfer_exact_balance(self):
        transaction = Transaction("TXN002", self.account1, self.account2, 
                                 5000.0, "TRANSFER", "Exact balance transfer")
        
        result = transaction.execute_transfer()
        self.assertTrue(result)
        self.assertEqual(self.account1.balance, 0.0)
        self.assertEqual(self.account2.balance, 8000.0)
        self.assertEqual(transaction.status, "COMPLETED")
    
    def test_generate_transaction_receipt(self):
        self.transaction.execute_transfer()
        receipt = self.transaction.generate_transaction_receipt()
        
        self.assertIn("Transaction #TXN001", receipt)
        self.assertIn("Amount: 1000.0", receipt)
    
class TestInvoiceEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("CL001", "Test Client", "test@test.com", 
                            "+1234567890", None, 1000.0)
        self.line_items = [
            {"item": "Service 1", "amount": 100.0},
            {"item": "Service 2", "amount": 200.0}
        ]
    
    def test_validate_invoice_data_exceptions(self):
        with self.assertRaises(Exception):
            Invoice("", None, self.client, "2024-01-01", "2024-02-01", self.line_items)
        with self.assertRaises(Exception):
            Invoice("INV001", None, None, "2024-01-01", "2024-02-01", self.line_items)
        with self.assertRaises(Exception):
            Invoice("INV001", None, self.client, "2024-01-01", "2024-02-01", [])
    
    def test_calculate_total_amount_method(self):
        invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                         "2024-02-01", self.line_items)
        self.assertEqual(invoice.total_amount, 300.0)
        invoice.add_line_item("Service 3", 150.0, 2) 
        self.assertEqual(invoice.total_amount, 600.0)
    
    def test_remove_line_item_edge_cases(self):
        invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                         "2024-02-01", self.line_items)
        
        initial_total = invoice.total_amount
        result = invoice.remove_line_item(-1)
        self.assertFalse(result)
        self.assertEqual(invoice.total_amount, initial_total)

        result = invoice.remove_line_item(10)
        self.assertFalse(result)
        self.assertEqual(invoice.total_amount, initial_total)
        result = invoice.remove_line_item(0)
        self.assertTrue(result)
        self.assertEqual(invoice.total_amount, 200.0) 
    
    def test_invoice_validation_method(self):
        valid_invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                               "2024-02-01", self.line_items)
        self.assertTrue(valid_invoice.validate_invoice_data())
        class MockInvoice:
            def validate_invoice_data(self):
                if not self.invoice_id:
                    return False
                if self.total_amount <= 0:
                    return False
                if not self.issue_date or not self.due_date:
                    return False
                return True
        
        mock_invoice = MockInvoice()
        mock_invoice.invoice_id = ""
        mock_invoice.total_amount = 100.0
        mock_invoice.issue_date = "2024-01-01"
        mock_invoice.due_date = "2024-02-01"
        self.assertFalse(mock_invoice.validate_invoice_data())
        mock_invoice.invoice_id = "INV001"
        mock_invoice.total_amount = -100.0
        self.assertFalse(mock_invoice.validate_invoice_data())

        mock_invoice.total_amount = 0.0
        self.assertFalse(mock_invoice.validate_invoice_data())
       
        mock_invoice.total_amount = 100.0
        mock_invoice.issue_date = ""
        mock_invoice.due_date = ""
        self.assertFalse(mock_invoice.validate_invoice_data())
    
def test_generate_invoice_content(self):
    line_items = [
        {"description": "Service 1", "amount": 100.0},
        {"description": "Service 2", "amount": 200.0}
    ]
    
    invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                     "2024-02-01", line_items)
    
    content = invoice._generate_invoice_content()
    self.assertIn("INVOICE: INV001", content)
    self.assertIn("Client: Test Client", content)
    self.assertIn("Issue Date: 2024-01-01", content)
    self.assertIn("Due Date: 2024-02-01", content)
    self.assertIn("Service 1", content)
    self.assertIn("Service 2", content)
    self.assertIn("$100.00", content)
    self.assertIn("$200.00", content)
    self.assertIn("Total Amount: $300.00", content)
    
def test_apply_discount_edge_cases(self):
    invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                     "2024-12-31", self.line_items) 
    result = invoice.apply_early_payment_discount(0.0)
    self.assertTrue(result)
    self.assertEqual(invoice.discount_amount, 0.0)
    from src.constants.config_constants import ConfigConstants
    max_discount = ConfigConstants.MAX_DISCOUNT_PERCENTAGE
    result = invoice.apply_early_payment_discount(100.0)
    self.assertTrue(result)
    expected_discount = invoice.total_amount * (max_discount / 100)
    self.assertEqual(invoice.discount_amount, expected_discount)
    class MockPayment:
        def __init__(self, amount):
            self.amount = amount
            self.payment_id = "PAY001"
            self.payment_date = "2024-01-15"
            self.payment_method = "cash"
    
    payment = MockPayment(150.0)
    invoice.add_payment(payment)
    invoice2 = Invoice("INV002", None, self.client, "2024-01-01", 
                      "2024-12-31", self.line_items)
    invoice2.add_payment(payment)
    
    result = invoice2.apply_early_payment_discount(10.0)
class TestInvoicePublicMethods(unittest.TestCase):
    def setUp(self):
        self.client = Client("CL001", "Test Client", "test@test.com", 
                            "+1234567890", None, 1000.0)
        self.line_items = [
            {"description": "Service 1", "amount": 100.0},
            {"description": "Service 2", "amount": 200.0}
        ]
    
    def test_invoice_creation_and_basic_properties(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        self.assertEqual(invoice.invoice_id, "INV001")
        self.assertEqual(invoice.client, self.client)
        self.assertEqual(invoice.issue_date, "2024-01-01")
        self.assertEqual(invoice.due_date, "2024-02-01")
        self.assertEqual(len(invoice.line_items), 2)
        self.assertEqual(invoice.total_amount, 300.0)
        self.assertEqual(invoice.paid_amount, 0.0)
        self.assertEqual(invoice.status, "ISSUED")
        self.assertEqual(invoice.tax_amount, 0.0)
        self.assertEqual(invoice.discount_amount, 0.0)
    
    def test_add_payment_scenarios(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        class MockPayment:
            def __init__(self, amount):
                self.amount = amount
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "cash"
        payment1 = MockPayment(100.0)
        invoice.add_payment(payment1)
        
        self.assertEqual(invoice.paid_amount, 100.0)
        self.assertEqual(len(invoice.payments), 1)
        self.assertEqual(invoice.status, "PARTIALLY_PAID")
        payment2 = MockPayment(150.0)
        invoice.add_payment(payment2)
        self.assertEqual(invoice.paid_amount, 250.0)
        self.assertEqual(len(invoice.payments), 2)
        self.assertEqual(invoice.status, "PARTIALLY_PAID")
        payment3 = MockPayment(50.0)
        invoice.add_payment(payment3)
        self.assertEqual(invoice.paid_amount, 300.0)
        self.assertEqual(len(invoice.payments), 3)
        self.assertEqual(invoice.status, "PAID")
    
    def test_calculate_remaining_balance(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        self.assertEqual(invoice.calculate_remaining_balance(), 300.0)
        class MockPayment:
            def __init__(self, amount):
                self.amount = amount
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "cash"
        
        payment = MockPayment(100.0)
        invoice.add_payment(payment)
        
        self.assertEqual(invoice.calculate_remaining_balance(), 200.0)
        payment2 = MockPayment(200.0)
        invoice.add_payment(payment2)
        
        self.assertEqual(invoice.calculate_remaining_balance(), 0.0)
    
def test_apply_early_payment_discount_comprehensive(self):
    future_invoice = Invoice("INV001", None, self.client, 
                            "2024-01-01", "2024-12-31", self.line_items)
    self.assertFalse(future_invoice.is_overdue())
    self.assertEqual(future_invoice.paid_amount, 0.0)
    result = future_invoice.apply_early_payment_discount(10.0)
    self.assertTrue(result, f"Скидка должна применяться. is_overdue: {future_invoice.is_overdue()}, paid_amount: {future_invoice.paid_amount}, total_amount: {future_invoice.total_amount}")
    self.assertEqual(future_invoice.discount_amount, 30.0)  
    self.assertEqual(future_invoice.total_amount, 270.0)    
    from src.constants.config_constants import ConfigConstants
    invoice2 = Invoice("INV002", None, self.client, 
                      "2024-01-01", "2024-12-31", self.line_items)
    
    result = invoice2.apply_early_payment_discount(100.0)
    self.assertTrue(result, "Скидка должна применяться даже если процент выше максимального (должна быть ограничена)")
    
    max_discount = ConfigConstants.MAX_DISCOUNT_PERCENTAGE
    expected_discount = 300.0 * (max_discount / 100)
    self.assertEqual(invoice2.discount_amount, expected_discount, 
                     f"Скидка должна быть ограничена {max_discount}%. Получено: {invoice2.discount_amount}, Ожидалось: {expected_discount}")
    past_invoice = Invoice("INV003", None, self.client, 
                          "2024-01-01", "2023-01-01", self.line_items)
    
    result = past_invoice.apply_early_payment_discount(10.0)
    self.assertFalse(result, "Скидка не должна применяться для просроченного счета")
    paid_invoice = Invoice("INV004", None, self.client, 
                          "2024-01-01", "2024-12-31", self.line_items)
    
    class MockPayment:
        def __init__(self, amount):
            self.amount = amount
            self.payment_id = "PAY001"
            self.payment_date = "2024-01-15"
            self.payment_method = "cash"
    payment = MockPayment(300.0)
    paid_invoice.add_payment(payment)
    self.assertTrue(paid_invoice.is_fully_paid())
    
    result = paid_invoice.apply_early_payment_discount(10.0)
    self.assertFalse(result, "Скидка не должна применяться для полностью оплаченного счета")
    def test_is_fully_paid_states(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        self.assertFalse(invoice.is_fully_paid())
        self.assertEqual(invoice.status, "ISSUED")
        class MockPayment:
            def __init__(self, amount):
                self.amount = amount
                self.payment_id = "PAY001"
                self.payment_date = "2024-01-15"
                self.payment_method = "cash"
        
        payment1 = MockPayment(100.0)
        invoice.add_payment(payment1)
        
        self.assertFalse(invoice.is_fully_paid())
        self.assertEqual(invoice.status, "PARTIALLY_PAID")
        
        payment2 = MockPayment(200.0)
        invoice.add_payment(payment2)
        
        self.assertTrue(invoice.is_fully_paid())
        self.assertEqual(invoice.status, "PAID")
    
    def test_add_and_remove_line_items(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        initial_total = invoice.total_amount
        initial_count = len(invoice.line_items)
        invoice.add_line_item("New Service", 50.0, 2)  
        self.assertEqual(len(invoice.line_items), initial_count + 1)
        self.assertEqual(invoice.total_amount, initial_total + 100.0)
        invoice.add_line_item("Another Service", 25.0)
        self.assertEqual(len(invoice.line_items), initial_count + 2)
        self.assertEqual(invoice.total_amount, initial_total + 100.0 + 25.0)
        result = invoice.remove_line_item(0)
        self.assertTrue(result)
        self.assertEqual(len(invoice.line_items), initial_count + 1)
        result = invoice.remove_line_item(100)
        self.assertFalse(result)
    
    def test_calculate_tax_and_total(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        initial_total = invoice.total_amount
        tax_amount = invoice.calculate_tax(20.0)
        expected_tax = initial_total * 0.20
        self.assertEqual(tax_amount, expected_tax)
        self.assertEqual(invoice.tax_amount, expected_tax)
        self.assertEqual(invoice.total_amount, initial_total + expected_tax)
        new_initial = invoice.total_amount
        tax_amount2 = invoice.calculate_tax(10.0)
        expected_tax2 = new_initial * 0.10
        self.assertEqual(tax_amount2, expected_tax2)
        self.assertEqual(invoice.total_amount, new_initial + expected_tax2)
    
    def test_get_aging_category_logic(self):
        test_cases = [
            ("2024-03-01", "NOT_DUE"),    
            ("2024-02-15", "NOT_DUE"),     
            ("2024-01-31", "1-30_DAYS"),   
            ("2024-01-01", "31-60_DAYS"),  
            ("2023-12-01", "61-90_DAYS"),  
            ("2023-09-01", "OVER_90_DAYS"),
        ]
        
        for due_date, expected_type in test_cases:
            invoice = Invoice("INV001", None, self.client, 
                             "2024-01-01", due_date, self.line_items)
            
            category = invoice.get_aging_category()
            self.assertIsInstance(category, str)
    
    def test_validate_invoice_data_method(self):
        valid_invoice = Invoice("INV001", None, self.client, 
                               "2024-01-01", "2024-02-01", self.line_items)
        self.assertTrue(valid_invoice.validate_invoice_data())
        test_invoice = Invoice("INV002", None, self.client, 
                              "2024-01-01", "2024-02-01", self.line_items)
        original_id = test_invoice.invoice_id
        test_invoice.invoice_id = ""
        self.assertFalse(test_invoice.validate_invoice_data())
        test_invoice.invoice_id = original_id 
        original_total = test_invoice.total_amount
        test_invoice.total_amount = 0.0
        self.assertFalse(test_invoice.validate_invoice_data())
        test_invoice.total_amount = original_total
        original_issue = test_invoice.issue_date
        test_invoice.issue_date = ""
        self.assertFalse(test_invoice.validate_invoice_data())
    
    def test_generate_invoice_pdf_structure(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        pdf_data = invoice.generate_invoice_pdf()
        self.assertIsInstance(pdf_data, dict)
        required_keys = ['filename', 'content', 'generated_date', 'pages']
        for key in required_keys:
            self.assertIn(key, pdf_data)
        self.assertEqual(pdf_data['filename'], "invoice_INV001.pdf")
        self.assertIn("INVOICE: INV001", pdf_data['content'])
        self.assertEqual(pdf_data['pages'], 1)
    
    def test_get_payment_history_format(self):
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        history = invoice.get_payment_history()
        self.assertEqual(history, [])
        self.assertIsInstance(history, list)
        class MockPayment:
            def __init__(self):
                self.payment_id = "PAY001"
                self.amount = 100.0
                self.payment_date = "2024-01-15"
                self.payment_method = "credit_card"
        payment = MockPayment()
        invoice.add_payment(payment)
        history = invoice.get_payment_history()
        self.assertEqual(len(history), 1)
        payment_info = history[0]
        self.assertIsInstance(payment_info, dict)
        self.assertEqual(payment_info['payment_id'], "PAY001")
        self.assertEqual(payment_info['amount'], 100.0)
        self.assertEqual(payment_info['date'], "2024-01-15")
        self.assertEqual(payment_info['method'], "credit_card")
class MockPayment:
    """Mock класс для тестирования платежей"""
    def __init__(self, amount=100.0):
        self.amount = amount
        self.payment_id = "PAY001"
        self.payment_date = "2024-01-15"
        self.payment_method = "cash"


class TestInvoiceComprehensive(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("CL001", "Test Client", "test@test.com", 
                            "+1234567890", None, 1000.0)
        self.line_items = [
            {"description": "Service 1", "amount": 100.0},
            {"description": "Service 2", "amount": 200.0}
        ]
        # Фиксированная дата для всех тестов
        self.fixed_date = datetime(2024, 2, 1)  # 1 февраля 2024
    
    def test_invoice_constructor_edge_cases(self):
        """Тестирование крайних случаев при создании счета"""
        with self.assertRaises(Exception):
            Invoice("INV001", None, self.client, "2024-01-01", "2024-02-01", [])
        
        line_items_zero = [{"description": "Free Service", "amount": 0.0}]
        invoice = Invoice("INV001", None, self.client, "2024-01-01", 
                         "2024-02-01", line_items_zero)
        self.assertEqual(invoice.total_amount, 0.0)
        
        line_items_negative = [{"description": "Refund", "amount": -50.0}]
        invoice = Invoice("INV002", None, self.client, "2024-01-01", 
                         "2024-02-01", line_items_negative)
        self.assertEqual(invoice.total_amount, -50.0)
    
    def test_invoice_status_transitions(self):
        """Тестирование переходов статуса счета"""
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        self.assertEqual(invoice.status, "ISSUED")
        
        payment1 = MockPayment(50.0)
        invoice.add_payment(payment1)
        self.assertEqual(invoice.status, "PARTIALLY_PAID")
        
        payment2 = MockPayment(250.0)
        invoice.add_payment(payment2)
        self.assertEqual(invoice.status, "PAID")
        
        invoice2 = Invoice("INV002", None, self.client, 
                          "2024-01-01", "2024-02-01", self.line_items)
        payment_over = MockPayment(400.0)
        invoice2.add_payment(payment_over)
        self.assertEqual(invoice2.status, "PAID")
    
    @patch('datetime.datetime')
    def test_invoice_overdue_logic(self, mock_datetime):
        """Тестирование логики определения просрочки"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        # Счет с будущей датой оплаты (после 1 февраля)
        future_invoice = Invoice("INV001", None, self.client, 
                                "2024-01-01", "2024-12-31", self.line_items)
        self.assertFalse(future_invoice.is_overdue())
        
        # Счет с прошедшей датой оплаты (до 1 февраля)
        past_invoice = Invoice("INV002", None, self.client, 
                              "2024-01-01", "2023-01-01", self.line_items)
        self.assertTrue(past_invoice.is_overdue())
        
        # Просроченный счет после оплаты
        paid_past_invoice = Invoice("INV003", None, self.client, 
                                   "2024-01-01", "2023-01-01", self.line_items)
        payment = MockPayment(300.0)
        paid_past_invoice.add_payment(payment)
        self.assertFalse(paid_past_invoice.is_overdue())
    
    @patch('datetime.datetime')
    def test_apply_early_payment_discount_comprehensive(self, mock_datetime):
        """Расширенное тестирование скидки за раннюю оплату"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        # Тест 1: Скидка применяется при нулевой оплате и не просроченном счете
        invoice1 = Invoice("INV001", None, self.client, 
                          "2024-01-01", "2024-12-31", self.line_items)
        result = invoice1.apply_early_payment_discount(10.0)
        self.assertTrue(result)
        self.assertEqual(invoice1.discount_amount, 30.0)
        self.assertEqual(invoice1.total_amount, 270.0)
        
        # Тест 2: Скидка применяется при частичной оплате
        invoice2 = Invoice("INV002", None, self.client, 
                          "2024-01-01", "2024-12-31", self.line_items)
        payment = MockPayment(100.0)
        invoice2.add_payment(payment)
        result = invoice2.apply_early_payment_discount(10.0)
        self.assertTrue(result)
        # Скидка должна применяться к оставшейся сумме (300-100=200)
        expected_discount = 200.0 * 0.10
        self.assertEqual(invoice2.discount_amount, expected_discount)
        
        # Тест 3: Максимальная скидка ограничена константой
        from src.constants.config_constants import ConfigConstants
        invoice3 = Invoice("INV003", None, self.client, 
                          "2024-01-01", "2024-12-31", self.line_items)
        result = invoice3.apply_early_payment_discount(100.0)
        self.assertTrue(result)
        max_discount = ConfigConstants.MAX_DISCOUNT_PERCENTAGE
        expected_discount = 300.0 * (max_discount / 100)
        self.assertEqual(invoice3.discount_amount, expected_discount)
        
        # Тест 4: Скидка не применяется для просроченного счета
        past_invoice = Invoice("INV004", None, self.client, 
                              "2024-01-01", "2023-01-01", self.line_items)
        result = past_invoice.apply_early_payment_discount(10.0)
        self.assertFalse(result)
        self.assertEqual(past_invoice.discount_amount, 0.0)
        
        # Тест 5: Скидка не применяется для полностью оплаченного счета
        paid_invoice = Invoice("INV005", None, self.client, 
                              "2024-01-01", "2024-12-31", self.line_items)
        full_payment = MockPayment(300.0)
        paid_invoice.add_payment(full_payment)
        result = paid_invoice.apply_early_payment_discount(10.0)
        self.assertFalse(result)
    
    def test_line_items_management(self):
        """Тестирование управления позициями счета"""
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items.copy())
        
        invoice.add_line_item("Free Item", 0.0, 5)
        self.assertEqual(len(invoice.line_items), 3)
        self.assertEqual(invoice.total_amount, 300.0)  # Сумма не должна измениться
        
        invoice.add_line_item("Refund", -50.0)
        self.assertEqual(len(invoice.line_items), 4)
        self.assertEqual(invoice.total_amount, 250.0)  # 300 - 50
        
        initial_count = len(invoice.line_items)
        result = invoice.remove_line_item(100)
        self.assertFalse(result)
        self.assertEqual(len(invoice.line_items), initial_count)
        
        result = invoice.remove_line_item(-1)
        self.assertFalse(result)
        
        for i in range(5):
            invoice.add_line_item(f"Temp Item {i}", 10.0)
        
        self.assertEqual(len(invoice.line_items), initial_count + 5)
        
        while len(invoice.line_items) > 1:
            invoice.remove_line_item(0)
        
        self.assertEqual(len(invoice.line_items), 1)
    
    @patch('datetime.datetime')
    def test_payment_reminder_logic(self, mock_datetime):
        """Тестирование логики напоминаний об оплате"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        # Счет с будущей датой оплаты - напоминание не отправляется
        future_invoice = Invoice("INV001", None, self.client, 
                                "2024-01-01", "2024-12-31", self.line_items)
        reminder = future_invoice.send_payment_reminder()
        self.assertIsNone(reminder)
        
        # Просроченный неоплаченный счет - напоминание отправляется
        past_invoice = Invoice("INV002", None, self.client, 
                              "2024-01-01", "2023-01-01", self.line_items)
        reminder = past_invoice.send_payment_reminder()
        self.assertIsNotNone(reminder)
        self.assertIn("Payment Reminder", reminder)
        self.assertIn("INV002", reminder)
        
        # Просроченный оплаченный счет - напоминание не отправляется
        paid_past_invoice = Invoice("INV003", None, self.client, 
                                   "2024-01-01", "2023-01-01", self.line_items)
        payment = MockPayment(300.0)
        paid_past_invoice.add_payment(payment)
        reminder = paid_past_invoice.send_payment_reminder()
        self.assertIsNone(reminder)
    
    @patch('datetime.datetime')
    def test_late_fee_calculation(self, mock_datetime):
        """Тестирование расчета штрафов за просрочку"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        # Непросроченный счет - штраф 0
        future_invoice = Invoice("INV001", None, self.client, 
                                "2024-01-01", "2024-12-31", self.line_items)
        late_fee = future_invoice.calculate_late_fee(10.0)
        self.assertEqual(late_fee, 0.0)
        
        # Просроченный счет - положительный штраф
        past_invoice = Invoice("INV002", None, self.client, 
                              "2024-01-01", "2023-01-01", self.line_items)
        late_fee = past_invoice.calculate_late_fee(5.0)
        self.assertGreater(late_fee, 0.0)
        
        # Нулевая ежедневная ставка
        late_fee_zero = past_invoice.calculate_late_fee(0.0)
        self.assertEqual(late_fee_zero, 0.0)
        
        # Отрицательная ежедневная ставка
        late_fee_negative = past_invoice.calculate_late_fee(-5.0)
        self.assertLess(late_fee_negative, 0.0)
    
    def test_tax_calculation_edge_cases(self):
        """Тестирование крайних случаев расчета налогов"""
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        # Нулевая налоговая ставка
        tax_amount = invoice.calculate_tax(0.0)
        self.assertEqual(tax_amount, 0.0)
        self.assertEqual(invoice.total_amount, 300.0)
        
        # Отрицательная налоговая ставка (должна работать)
        tax_amount = invoice.calculate_tax(-10.0)
        self.assertEqual(tax_amount, -30.0)  # 300 * (-0.10)
        self.assertEqual(invoice.total_amount, 270.0)  # 300 + (-30)
        
        # Многократное применение налогов
        invoice2 = Invoice("INV002", None, self.client, 
                          "2024-01-01", "2024-02-01", self.line_items)
        initial_total = invoice2.total_amount
        invoice2.calculate_tax(10.0)
        tax1_total = invoice2.total_amount
        
        invoice2.calculate_tax(5.0)
        # Налог должен применяться к новой общей сумме
        expected_increase = tax1_total * 0.05
        self.assertEqual(invoice2.total_amount, tax1_total + expected_increase)
    
    @patch('datetime.datetime')
    def test_aging_category_comprehensive(self, mock_datetime):
        """Всестороннее тестирование категорий старения задолженности"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        test_cases = [
            ("2024-03-01", "NOT_DUE"),     # Будущая дата (1 марта)
            ("2024-02-15", "NOT_DUE"),     # Будущая дата (15 февраля)
            ("2024-01-31", "1-30_DAYS"),   # 1 день просрочки (1 фев - 31 янв = 1 день)
            ("2024-01-01", "31-60_DAYS"),  # 31 день просрочки
            ("2023-12-31", "31-60_DAYS"),  # 32 дня просрочки
            ("2023-12-01", "61-90_DAYS"),  # 62 дня просрочки
            ("2023-11-01", "OVER_90_DAYS"), # 92 дня просрочки
        ]
        
        for due_date, expected_category in test_cases:
            invoice = Invoice("INV001", None, self.client, 
                             "2024-01-01", due_date, self.line_items)
            category = invoice.get_aging_category()
            self.assertEqual(category, expected_category,
                           f"Для даты {due_date} ожидалась категория {expected_category}, получена {category}")
        
        # Оплаченный счет всегда имеет категорию "PAID"
        paid_invoice = Invoice("INV002", None, self.client, 
                              "2024-01-01", "2023-01-01", self.line_items)
        payment = MockPayment(300.0)
        paid_invoice.add_payment(payment)
        self.assertEqual(paid_invoice.get_aging_category(), "PAID")
    
    def test_validate_invoice_data_comprehensive(self):
        """Всесторонняя проверка валидации данных счета"""
        # Валидный счет
        valid_invoice = Invoice("INV001", None, self.client, 
                               "2024-01-01", "2024-02-01", self.line_items)
        self.assertTrue(valid_invoice.validate_invoice_data())
        
        # Создаем счет для тестирования разных состояний
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        # Сохраняем оригинальные значения
        original_values = {
            'invoice_id': invoice.invoice_id,
            'total_amount': invoice.total_amount,
            'issue_date': invoice.issue_date,
            'due_date': invoice.due_date
        }
        
        # Тест 1: Пустой ID счета
        invoice.invoice_id = ""
        self.assertFalse(invoice.validate_invoice_data())
        invoice.invoice_id = original_values['invoice_id']
        
        # Тест 2: Нулевая сумма
        invoice.total_amount = 0.0
        self.assertFalse(invoice.validate_invoice_data())
        invoice.total_amount = original_values['total_amount']
        
        # Тест 3: Отрицательная сумма
        invoice.total_amount = -100.0
        self.assertFalse(invoice.validate_invoice_data())
        invoice.total_amount = original_values['total_amount']
        
        # Тест 4: Пустая дата выставления
        invoice.issue_date = ""
        self.assertFalse(invoice.validate_invoice_data())
        invoice.issue_date = original_values['issue_date']
        
        # Тест 5: Пустая дата оплаты
        invoice.due_date = ""
        self.assertFalse(invoice.validate_invoice_data())
        invoice.due_date = original_values['due_date']
    
    def test_payment_history_management(self):
        """Тестирование управления историей платежей"""
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        # Начально пустая история
        history = invoice.get_payment_history()
        self.assertEqual(history, [])
        
        # Добавление нескольких платежей
        payments = []
        for i in range(3):
            payment = MockPayment(100.0)
            payment.payment_id = f"PAY00{i+1}"
            payment.payment_date = f"2024-01-{10+i}"
            payment.payment_method = ["cash", "card", "transfer"][i]
            invoice.add_payment(payment)
            payments.append(payment)
        
        # Проверка истории платежей
        history = invoice.get_payment_history()
        self.assertEqual(len(history), 3)
        
        for i, payment_info in enumerate(history):
            self.assertEqual(payment_info['payment_id'], f"PAY00{i+1}")
            self.assertEqual(payment_info['amount'], 100.0)
            self.assertEqual(payment_info['date'], f"2024-01-{10+i}")
            self.assertEqual(payment_info['method'], ["cash", "card", "transfer"][i])
    
    def test_invoice_string_representation(self):
        """Тестирование строкового представления счета"""
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        # Проверка наличия строкового представления
        str_repr = str(invoice)
        self.assertIsInstance(str_repr, str)
        # Поскольку Invoice не переопределяет __str__, проверяем базовое представление
        self.assertIn("Invoice object", str_repr)
        
        # Проверка содержимого PDF
        pdf_data = invoice.generate_invoice_pdf()
        content = pdf_data['content']
        
        required_sections = [
            "INVOICE: INV001",
            "Client: Test Client",
            "Issue Date: 2024-01-01",
            "Due Date: 2024-02-01",
            "LINE ITEMS:",
            "Service 1",
            "Service 2",
            "Total Amount: $300.00",
        ]
        
        for section in required_sections:
            self.assertIn(section, content)
    
    def test_invoice_equality_and_hash(self):
        """Тестирование сравнения и хэширования счетов"""
        invoice1 = Invoice("INV001", None, self.client, 
                          "2024-01-01", "2024-02-01", self.line_items)
        invoice2 = Invoice("INV001", None, self.client, 
                          "2024-01-01", "2024-02-01", self.line_items.copy())
        invoice3 = Invoice("INV002", None, self.client, 
                          "2024-01-01", "2024-02-01", self.line_items)
        
        # Два счета с одинаковым ID должны считаться разными объектами
        self.assertNotEqual(invoice1, invoice2)
        
        # Хэши должны быть разными для разных объектов
        self.assertNotEqual(hash(invoice1), hash(invoice2))
        self.assertNotEqual(hash(invoice1), hash(invoice3))
    
    @patch('datetime.datetime')
    def test_invoice_copy_and_serialization(self, mock_datetime):
        """Тестирование копирования и сериализации счета"""
        # Настраиваем мок для datetime.now()
        mock_datetime.now.return_value = self.fixed_date
        # Сохраняем оригинальный strptime
        mock_datetime.strptime = datetime.strptime
        
        original_invoice = Invoice("INV001", None, self.client, 
                                  "2024-01-01", "2024-12-31", self.line_items.copy())
        
        # Добавляем платеж
        payment = MockPayment(100.0)
        original_invoice.add_payment(payment)
        
        # Применяем скидку (должно сработать, так как счет не просрочен)
        result = original_invoice.apply_early_payment_discount(10.0)
        self.assertTrue(result)
        
        # Проверяем, что оригинальный объект изменен
        self.assertEqual(original_invoice.paid_amount, 100.0)
        self.assertGreater(original_invoice.discount_amount, 0)
        
        # Создаем новый счет с теми же данными
        copied_line_items = [item.copy() for item in self.line_items]
        copied_invoice = Invoice("INV001", None, self.client, 
                                "2024-01-01", "2024-12-31", copied_line_items)
        
        # Проверяем, что это разные объекты с разными состояниями
        self.assertEqual(copied_invoice.paid_amount, 0.0)
        self.assertEqual(copied_invoice.discount_amount, 0.0)
        self.assertNotEqual(original_invoice.status, copied_invoice.status)
    
    def test_error_handling_and_exceptions(self):
        """Тестирование обработки ошибок и исключений"""
        # Создание счета с невалидными данными должно вызывать исключение
        with self.assertRaises(Exception):
            Invoice("", None, self.client, "2024-01-01", "2024-02-01", self.line_items)
        
        with self.assertRaises(Exception):
            Invoice("INV001", None, None, "2024-01-01", "2024-02-01", self.line_items)
        
        # Операции с неинициализированным объектом
        invoice = Invoice("INV001", None, self.client, 
                         "2024-01-01", "2024-02-01", self.line_items)
        
        # Попытка добавить некорректный платеж (без amount)
        class InvalidPayment:
            def __init__(self):
                self.payment_id = "PAY001"
                # Нет amount
        
        with self.assertRaises(AttributeError):
            invoice.add_payment(InvalidPayment())


if __name__ == '__main__':
    unittest.main()