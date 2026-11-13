# Item 75: Use Repr Strings for Debugging Output

# 1. Default Output from print() --> No way of distinguishing the actual type and its specific composition
my_value = 'Hello World!'
print(str(my_value))
print('%s' % my_value)
print(f'{my_value}')
print(format(my_value))
print(my_value.__format__('s'))
print(my_value.__str__())

int_value = 42
str_value = '42'
print(f'{int_value} == {str_value}?')

# Solution: Use repr() to get a string representation of the object that includes the type
print(repr(int_value))
print(repr(str_value))

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Object(x={self.x}, y={self.y})'

obj_1 = Object(1, '2')

# define my own __repr__ special method that returns a string containing the 
# Python expression that re-creates the object
print(f"__repr__: {obj_1.__repr__()}") 

# Use dictionary when there is no control of the class definition
print(f"__dict__: {obj_1.__dict__}") 






