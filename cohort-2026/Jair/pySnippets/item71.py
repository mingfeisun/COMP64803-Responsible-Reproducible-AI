
from collections import deque

# Each order contains an ID, a product, and a quantity
orders = deque([
    {"id": 115, "product": "Laptop", "quantity": 1},
    {"id": 322, "product": "Mouse", "quantity": 2},
    {"id": 479, "product": "Keyboard", "quantity": 1},
    {"id": 556, "product": "Monitor", "quantity": 2},
])

processed_orders = []
total_items = 0

# Process orders in the order they arrived
while orders:
    current_order = orders.popleft()

    order_id = current_order["id"]
    product = current_order["product"]
    quantity = current_order["quantity"]

    print(f"Processing Order {order_id}")
    print(f"Product: {product}")
    print(f"Quantity: {quantity}")
    print("-" * 30)

    processed_orders.append(order_id)
    total_items += quantity

print(f"Orders processed: {len(processed_orders)}")
print(f"Order IDs: {processed_orders}")
print(f"Total items to ship: {total_items}")
