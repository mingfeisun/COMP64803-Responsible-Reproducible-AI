# Consider comprehensions instead of map/filter to make a list

data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ]

cubes = []
for x in data:
    if x < 30:
        cubes.append(x**3)
    else:
        pass

print(f'Method 1 (yuck):', cubes)


cubes = list(map(lambda x: x**3, filter(lambda x: x < 30, data)))
print(f'Method 2 (gross):', cubes)


sqsrt = [x**3 for x in data if x < 30]
print(f'Method 3 (nice!):', cubes)



