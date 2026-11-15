# Item 9: Avoid else Blocks After for and while Loops

# A normal for loop
print("Example 1: Normal for loop")

for i in range(3):
    print('Loop', i)
else:
    print('Else block!')


# A for loop with a break statement
print("\nExample 2: For loop with break")

for i in range(3):
    print('Loop', i)

    if i == 1:
        break
else:
    print('Else block!')