list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

first, *others, last = list
print(first, last, others)

*others, second_last, last = list
print(others, second_last, last)

first, second, *others = list
print(first, second, others)
