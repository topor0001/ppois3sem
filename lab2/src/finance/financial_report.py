from src.utils import manual_utils_instance as ManualUtils

class FinancialReport:
    def __init__(self, report_id, period_start, period_end, generated_by, transactions, invoices):
        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.generated_by = generated_by
        self.transactions = transactions
        self.invoices = invoices
        self.revenue = 0.0
        self.expenses = 0.0

    def calculate_financial_metrics(self):
        self.revenue = 0
        for inv in self.invoices:
            if inv.paid_amount > 0:
                self.revenue += inv.total_amount
        
        self.expenses = 0
        for tran in self.transactions:
            if tran.transaction_type == "EXPENSE":
                self.expenses += tran.amount
        
        return {
            'revenue': self.revenue,
            'expenses': self.expenses,
            'profit': self.revenue - self.expenses
        }

    def generate_report_summary(self):
        metrics = self.calculate_financial_metrics()
        return f"Financial Report {self.period_start}-{self.period_end}\nProfit: {metrics['profit']:.2f}"