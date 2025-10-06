# Sample list
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. Using a list comprehension to calculate squares
squares_comprehension = [x**2 for x in a]
print("Squares using comprehension:", squares_comprehension)

# 2. Using map (with lambda) to calculate squares
squares_map = list(map(lambda x: x**2, a))
print("Squares using map:", squares_map)

# 3. Using a list comprehension to calculate squares of even numbers
even_squares_comprehension = [x**2 for x in a if x % 2 == 0]
print("Even squares using comprehension:", even_squares_comprehension)

# 4. Using map and filter to calculate squares of even numbers
even_squares_map_filter = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, a)))
print("Even squares using map and filter:", even_squares_map_filter)
