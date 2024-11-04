from context_timer import Timer
import bisect 
import string 

# Searching a list! 
search_space = list(range(10000000))

goal = 9000000
# Linear search with timer.
with Timer() as timer: 
    for i, val in enumerate(search_space):
        if val == goal:
            print(f'Indices:{i}') 
            print(f'Value:{val}') 
            break


# Logarithmic search time (binomial search algorithm)
with Timer() as timer:
    i = bisect.bisect(search_space, goal)
    print(f'Indices:{i}') 


# In the case here we take the alphabet and do the combinatorics for 4 slots 
alphabet = string.ascii_lowercase

alphabet_list = [] 
for space_1 in alphabet:
    for space_2 in alphabet: 
        for space_3 in alphabet: 
            for space_4 in alphabet: 
                alphabet_list.append(space_1 + ',' + space_2  + ',' + space_3 + ',' + space_4)

# Getting the number of unique characters as a sudo function
def unique_characters(x): 
    unique_chars = set(x.split(','))
    return len(unique_chars) 

# Using a dictionary via a dict comprehension
linear_list = [[character, unique_characters(character)] for character in alphabet_list]
# Could just use dict (linear_list) here instead.
hash_set = {character: unique_characters(character) for character in alphabet_list}

# Setting the goal and evaluating linear search vs hash list
goal = 'z,z,z,y'
with Timer() as timer:
    for i, val in enumerate(linear_list): 
        if val[0] == goal: 
            count = val[1]
            print(f'There are {count} unique characters in {goal}')
            break 

with Timer() as timer: 
        count = hash_set[goal]
        print(f'There are {count} unique characters in {goal}')

