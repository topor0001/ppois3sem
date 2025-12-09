class QualityInspection:
    def __init__(self, inspection_id, repair_order, inspector, inspection_date, criteria):
        self.inspection_id = inspection_id
        self.repair_order = repair_order
        self.inspector = inspector
        self.inspection_date = inspection_date
        self.criteria = criteria
        self.passed = False

    def perform_inspection(self):
        self.passed = len(self.criteria) > 5