class PurchaseOrder:
    def __init__(self, order_id, supplier, items, order_date, expected_delivery, total_amount):
        self.order_id = order_id
        self.supplier = supplier
        self.items = items
        self.order_date = order_date
        self.expected_delivery = expected_delivery
        self.total_amount = total_amount
        self.status = "PENDING"
        self.received_items = []

def process_delivery(self, delivered_items):
    for item_data in delivered_items:
        item = item_data['item']
        quantity = item_data['quantity']
        item.restock_items(quantity)
        self.received_items.append(item_data)
    
    # Сравниваем количество полученных уникальных товаров
    # (не количество записей в списках)
    unique_received = len(set([item['item'].part_id for item in self.received_items]))
    unique_ordered = len(set([item.part_id for item in self.items]))
    
    if unique_received >= unique_ordered:
        self.status = "COMPLETED"