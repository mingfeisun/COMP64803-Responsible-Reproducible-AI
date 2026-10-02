# using itertools for iterators and generators

import itertools

print("\n----- 1. Linking Iterators Together -----")

# chain
it = itertools.chain([1, 2, 3], [4, 5, 6])
print("chain:", list(it))  

# repeat
it = itertools.repeat("hello", 3)
print("repeat:", list(it)) 

# cycle
it = itertools.cycle([1, 2])
print("cycle:", [next(it) for _ in range(10)])

# tee: split one iterator into multiple
it1, it2, it3 = itertools.tee(['first', 'second'], 3)
print("tee 1:", list(it1))
print("tee 2:", list(it2))
print("tee 3:", list(it3))

# zip_longest: zip with fill for uneven lengths
keys = ['a', 'b', 'c']
vals = [10, 20]
print("zip_longest:", list(itertools.zip_longest(keys, vals, fillvalue=None)))


print("\n----- 2. Filtering Iterators -----")

values = list(range(1, 11))

# islice: slice an iterator and step in fun way
print("islice 2..8 step2:", list(itertools.islice(values, 2, 8, 2)))

# takewhile: stop when condition becomes false
less_than_7 = lambda x: x < 7
print("takewhile:", list(itertools.takewhile(less_than_7, values)))

# dropwhile: skip until condition becomes false
print("dropwhile:", list(itertools.dropwhile(less_than_7, values)))

# filterfalse: return items where condition is False
evens = lambda x: x % 2 == 0
print("filterfalse:", list(itertools.filterfalse(evens, values)))


print("\n----- 3. Combinations and Reductions -----")

# accumulate: running totals or other binary ops
vals = [1, 2, 3, 4]
print("accumulate sum:", list(itertools.accumulate(vals)))

# product: mix two iterators 
print("product mixed:", list(itertools.product([1,2], ['a','b'])))

# permutations
print("permutations (2 of [1,2,3]):", list(itertools.permutations([1,2,3], 2)))

# combinations
print("combinations (2 of [1,2,3,4]):", list(itertools.combinations([1,2,3,4], 2)))


