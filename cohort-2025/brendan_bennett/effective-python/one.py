shopping_list = ["Tuesday", "apples", "carrots", "potatoes"]

print(shopping_list)

day, first, second, third = shopping_list

print(day, first, second, third)

for i, item in enumerate(shopping_list[1:]):
    print(i, item)