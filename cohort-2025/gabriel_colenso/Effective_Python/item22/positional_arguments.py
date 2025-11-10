def message_sum(message, *values):
    if not values:
        print(message)
    print(f'{message}: {sum(values)}')

numbers = [1, 3, 5]

assert message_sum('Sum of my numbers are', 1, 3, 5) == message_sum('Sum of my numbers are', *numbers)
