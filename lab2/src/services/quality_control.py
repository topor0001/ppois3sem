class QualityControlManager:
    def __init__(self):
        self.quality_standards = []
        self.inspections = []
        self.quality_metrics = []

    def perform_quality_inspection(self, repair_order, inspector, criteria):
        from src.models.quality_inspection import QualityInspection
        inspection = QualityInspection(f"INS{len(self.inspections)}", repair_order, inspector, "2024-01-01", criteria)
        inspection.perform_inspection()
        self.inspections.append(inspection)
        return inspection.passed

    def generate_quality_report(self):
        passed_count = 0
        for inspection in self.inspections:
            if inspection.passed:
                passed_count += 1
        
        total_count = len(self.inspections)
        success_rate = (passed_count / total_count * 100) if total_count > 0 else 0
        
        return f"Quality Report: {passed_count}/{total_count} passed ({success_rate:.1f}%)"