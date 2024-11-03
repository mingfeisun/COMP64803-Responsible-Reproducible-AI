import traceback 
import sys 

# Sudo dataset 
creatures = [
    {"name": "Dragon", "age": 500, "magic_level": 100},
    {"name": "Phoenix", "age": 1000, "magic_level": 95},
    {"name": "Unicorn", "age": 150, "magic_level": 80},
    {"name": "Goblin", "age": 30, "magic_level": 20},
    {"name": "Fairy", "age": 200, "magic_level": 85},
]

try: 
    creatures.sort()
except TypeError as e:
    e.add_note('This error arose as we cannot sort dict keys')
    traceback.print_exc() 
finally: 
    pass  

print('########################### SORTED BY AGE')

creatures.sort(key=lambda creature: creature["age"])
for creature in creatures:
    print(creature) 

print('########################### SORTED BY MAGIC LEVEL DESCENDING')

creatures.sort(key=lambda creature: creature["magic_level"], reverse=True)
for creature in creatures: 
    print(creature) 

print('########################### SORTED BY NAME LENGTH')

creatures.sort(key=lambda creature: len(creature["name"]))
for creature in creatures: 
    print(creature) 


# Naive example of implementing a sort algorithm 

# Bubble sort based on 'age' attribute
for i in range(len(creatures)):
    for j in range(0, len(creatures) - i - 1):
        if creatures[j]["age"] > creatures[j + 1]["age"]:
            # Swap if the current creature's age is greater than the next creature's age
            creatures[j], creatures[j + 1] = creatures[j + 1], creatures[j]

print("Sorted by age (without key):")
for creature in creatures: 
    print(creature) 

