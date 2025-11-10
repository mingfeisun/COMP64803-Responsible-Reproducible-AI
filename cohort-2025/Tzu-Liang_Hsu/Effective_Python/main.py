# 1: Item 2
print("==========The first item: PEP 8==========")
x: int = 5 # correct
print("Correct whitespace", x)
x :int=5 # wrong
print("Incorrect whitespace", x)


# 2: Item 8
print("\n==========The second item: zip==========")
# To calculate the total scores
students = ['Alice', 'Bob', 'Charlie', 'Diana']
test1 = [85, 91, 78, 95]
test2 = [88, 89, 82, 93]

# Range
for i in range(len(students)):
    total = test1[i] + test2[i]
    print(students[i], "total:", total)

# Enumerate
for i, name in enumerate(students):
    total = test1[i] + test2[i]
    print(name, "total:", total)

# Zip
for name, s1, s2 in zip(students, test1, test2):
    total = s1 + s2
    print(name, "total:", total)



# 3: Item 14
print("\n==========The third item: sort==========")
# Number
weights = [4, 5, 40, 4]
weights.sort()
print("Number list in ascending order:", weights)

# String
names = ['drill', 'circular saw','jackhammer', 'sander']
names.sort()
print("String list in ascending order:", names)

# Object
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

# Create an object
power_tools = [
Tool('drill', 4),
Tool('circular saw', 5),
Tool('jackhammer', 40),
Tool('sander', 4),
]
print('Unsorted:', repr(power_tools))

# To sort name
power_tools.sort(key=lambda x: x.name)
print('Name is sorted: ', power_tools)

# To sort both in the same directons
power_tools.sort(key=lambda x: (x.weight, x.name))
print("Both attributes are sorted in the same directons:", power_tools)

# In the opposite directions
power_tools.sort(key=lambda x: x.name)
power_tools.sort(key=lambda x: x.weight, reverse=True)
print("Both attributes are sorted in the opposite directons (Weight ↓ and then name ↑ ):", power_tools)


# 4: Item 22
print("\n==========The fourth item: *arg==========")
def log(message, values):
    """ No using *arg"""
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in 
                                values)
        print(f'{message}: {values_str}')
print("Without *arg")
log('My numbers are', [1, 2])
log('Hi there', [])

def log(message, *values):
    ''' With arg*'''
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in
                               values)
        print(f'{message}: {values_str}')
print("With *arg,")
log('My numbers are', 1, 2)
log('Hi there')


# 5: Item 75
print("\n==========The fifth item: repr==========")
print("Outputs an integer (hides type information)", 5)
print("Outputs a string (hides type information)", 5)

print("Shows the type information:", repr('5'))
print("Brings back:", eval(repr('5')))

class object:
    def __init__(self, x, y):
        self.x = x
        self.y =y

    def __repr__(self):
        return f'object({self.x}, {self.y})'
    
print("__repr__: ", repr(object(1, 5)))
print("__dict__: ", object(1,5).__dict__)