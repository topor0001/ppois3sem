class WarrantyClaim:
    def __init__(self, claim_id, warranty, repair_order, claim_date, description, supporting_docs):
        self.claim_id = claim_id
        self.warranty = warranty
        self.repair_order = repair_order
        self.claim_date = claim_date
        self.description = description
        self.supporting_docs = supporting_docs
        self.status = "SUBMITTED"
        self.approved_amount = 0.0

    def evaluate_claim(self, evaluator):
        if self.warranty.is_valid():
            self.status = "APPROVED"
            self.approved_amount = self.repair_order.total_cost * 0.8
            return True
        else:
            self.status = "REJECTED"
            return False