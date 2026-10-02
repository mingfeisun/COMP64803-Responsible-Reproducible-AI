# #before
# def normalise(numbers):
#     total = sum(numbers)
#     return [n / total for n in numbers]

# data = (x for x in range(1, 4))
# print(normalise(data))  # [0.16666666666666666, 0.3333333333333333, 0.5]
# print(normalise(data))  # [0.0, 0.0, 0.0]

#after
def normalise(numbers):
    numbers = list(numbers) 
    total = sum(numbers)
    return [n / total for n in numbers]

data = (x for x in range(1, 4))
print(normalise(data))  # [0.16666666666666666, 0.3333333333333333, 0.5]
print(normalise(data))  # [0.16666666666666666, 0.3333333333333333, 0.5]
