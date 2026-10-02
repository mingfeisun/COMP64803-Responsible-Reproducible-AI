def get_batches(quantity, batch_size):
    """Return the number of batches for a given quantity and batch size."""
    return quantity // batch_size

# Sample data
stock = {
    'item_a': 20,
    'item_b': 15,
    'item_c': 0,
}

order = ['item_a', 'item_b', 'item_c']

# Avoid repeated work in comprehensions
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# Print the result
print(found)  # Output: {'item_a': 2, 'item_b': 1}
