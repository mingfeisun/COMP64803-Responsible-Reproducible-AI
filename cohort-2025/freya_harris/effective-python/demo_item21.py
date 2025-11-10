# # before
# def create_multipliers():
#     return [lambda x: i * x for i in range(5)]

# funcs = create_multipliers()
# print([f(2) for f in funcs]) # [8, 8, 8, 8, 8]

# after
def create_multipliers():
    return [lambda x, i=i: i * x for i in range(5)]

funcs = create_multipliers()
print([f(2) for f in funcs]) # [0, 2, 4, 6, 8]
