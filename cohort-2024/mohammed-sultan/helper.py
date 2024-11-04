from urllib.parse import parse_qs

# Initial dictionary with query parameters
query_string = 'red=5&blue=0&green='
my_values = parse_qs(query_string, keep_blank_values=True)

# Complex way to parse and set default values without helper functions
red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)

print("Without helper function:")
print(f"Red: {red}, Green: {green}, Opacity: {opacity}")

# Using a helper function for readability and reusability
def get_first_int(values, key, default=0):
    """Retrieve the first integer from a list of query values."""
    found = values.get(key, [''])
    return int(found[0]) if found[0] else default

# Simplified usage with the helper function
red = get_first_int(my_values, 'red')
green = get_first_int(my_values, 'green')
opacity = get_first_int(my_values, 'opacity')

print("\nWith helper function:")
print(f"Red: {red}, Green: {green}, Opacity: {opacity}")