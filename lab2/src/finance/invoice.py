from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_payment_data_exception import InvalidPaymentDataException
from src.constants.config_constants import ConfigConstants

class Invoice:
    def __init__(self, invoice_id, repair_order, client, issue_date, due_date, line_items):
        self._validate_invoice_data(invoice_id, client, line_items)
        
        self.invoice_id = invoice_id
        self.repair_order = repair_order
        self.client = client
        self.issue_date = issue_date
        self.due_date = due_date
        self.line_items = line_items
        self.total_amount = self._calculate_total_amount()
        self.paid_amount = 0.0
        self.payments = []
        self.status = "ISSUED"
        self.tax_amount = 0.0
        self.discount_amount = 0.0

    def _validate_invoice_data(self, invoice_id, client, line_items):
        if not invoice_id:
            raise InvalidPaymentDataException("invoice_id", invoice_id)
        if client is None:
            raise InvalidPaymentDataException("client", client)
        if not line_items or ManualUtils.manual_len(line_items) == 0:
            raise InvalidPaymentDataException("line_items", "Empty line items")

    def _calculate_total_amount(self):
        total = 0.0
        for item in self.line_items:
            total += item['amount']
        return total

    def add_line_item(self, description, amount, quantity=1):
        new_item = {
            'description': description,
            'amount': amount * quantity,
            'quantity': quantity,
            'unit_price': amount
        }
        self.line_items.append(new_item)
        self.total_amount += new_item['amount']

    def remove_line_item(self, index):
        if 0 <= index < ManualUtils.manual_len(self.line_items):
            removed_item = self.line_items.pop(index)
            self.total_amount -= removed_item['amount']
            return True
        return False

    def add_payment(self, payment):
        self.payments.append(payment)
        self.paid_amount += payment.amount
        
        if self.paid_amount >= self.total_amount:
            self.status = "PAID"
        elif self.paid_amount > 0:
            self.status = "PARTIALLY_PAID"

    def is_overdue(self):
        from datetime import datetime
        current_date = datetime.now().date()
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return current_date > due_date and self.status != "PAID"

    def calculate_remaining_balance(self):
        return self.total_amount - self.paid_amount

    def apply_early_payment_discount(self, discount_percentage):
        
        # Ограничиваем максимальную скидку
        if discount_percentage > ConfigConstants.MAX_DISCOUNT_PERCENTAGE:
            discount_percentage = ConfigConstants.MAX_DISCOUNT_PERCENTAGE
        
        # Разрешаем скидку даже если есть частичная оплата
        if not self.is_overdue() and self.paid_amount < self.total_amount:
            # Рассчитываем скидку от оставшейся суммы
            remaining_balance = self.total_amount - self.paid_amount
            self.discount_amount = remaining_balance * (discount_percentage / 100)
            self.total_amount -= self.discount_amount
            return True
        
        return False

    def generate_invoice_pdf(self):
        invoice_content = self._generate_invoice_content()
        pdf_filename = f"invoice_{self.invoice_id}.pdf"
        
        pdf_data = {
            'filename': pdf_filename,
            'content': invoice_content,
            'generated_date': "2024-01-01",
            'pages': 1
        }
        return pdf_data

    def _generate_invoice_content(self):
        content = []
        content.append("=" * 50)
        content.append(f"INVOICE: {self.invoice_id}")
        content.append("=" * 50)
        content.append(f"Client: {self.client.name}")
        content.append(f"Issue Date: {self.issue_date}")
        content.append(f"Due Date: {self.due_date}")
        content.append(f"Status: {self.status}")
        content.append("-" * 50)
        content.append("LINE ITEMS:")
        
        for i, item in enumerate(self.line_items, 1):
            content.append(f"{i}. {item.get('description', 'Service')}: ${item['amount']:.2f}")
        
        content.append("-" * 50)
        content.append(f"Subtotal: ${self.total_amount + self.discount_amount:.2f}")
        
        if self.discount_amount > 0:
            content.append(f"Discount: -${self.discount_amount:.2f}")
        
        content.append(f"Total Amount: ${self.total_amount:.2f}")
        content.append(f"Paid Amount: ${self.paid_amount:.2f}")
        content.append(f"Remaining Balance: ${self.calculate_remaining_balance():.2f}")
        content.append("=" * 50)
        
        return ManualUtils.manual_join(content, "\n")

    def send_payment_reminder(self):
        if self.is_overdue() and self.status != "PAID":
            reminder_message = f"Payment Reminder for Invoice {self.invoice_id}\n"
            reminder_message += f"Amount Due: ${self.calculate_remaining_balance():.2f}\n"
            reminder_message += f"Original Due Date: {self.due_date}\n"
            reminder_message += "Please make payment as soon as possible."
            return reminder_message
        return None

    def calculate_late_fee(self, daily_rate):
        if self.is_overdue():
            from datetime import datetime
            due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            days_overdue = (current_date - due_date).days
            return days_overdue * daily_rate
        return 0.0

    def validate_invoice_data(self):
        if not self.invoice_id:
            return False
        if self.total_amount <= 0:
            return False
        if not self.issue_date or not self.due_date:
            return False
        return True

    def get_payment_history(self):
        payment_history = []
        for payment in self.payments:
            payment_info = {
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'date': payment.payment_date,
                'method': payment.payment_method
            }
            payment_history.append(payment_info)
        return payment_history

    def calculate_tax(self, tax_rate):
        self.tax_amount = self.total_amount * (tax_rate / 100)
        self.total_amount += self.tax_amount
        return self.tax_amount

    def is_fully_paid(self):
        return self.status == "PAID"

    def get_aging_category(self):
        if self.is_fully_paid():
            return "PAID"
        
        from datetime import datetime
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        days_past_due = (current_date - due_date).days
        
        if days_past_due < 0:
            return "NOT_DUE"
        elif days_past_due <= 30:
            return "1-30_DAYS"
        elif days_past_due <= 60:
            return "31-60_DAYS"
        elif days_past_due <= 90:
            return "61-90_DAYS"
        else:
            return "OVER_90_DAYS"