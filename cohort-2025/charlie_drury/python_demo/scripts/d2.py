# Consider generator expressions instead of building big lists

data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ]

cubes = (x**3 for x in data if x < 30)

# It's now an iterator, not a list
print(cubes)            # <generator object ...>
print(next(cubes))      
print(next(cubes))      
