# Item 8: Use Zip to Process Iterators in Parallel

names = ["Darren", "Charlie", "Bob"]
ages = [60, 40, 30]

for name, age in zip(names, ages):
    print(f"Age of {name}: {age}")

bmis = [23, 24, 19]
for name, age, bmi in zip(names, ages, bmis):
    print(f"{name} \n Age: {age}, BMI: {bmi}") 

# zip_longest
import itertools

names_2 = ["Darren", "Charlie", "Bob", "Jack"]
bmis_2 = [23, 24, 19]
for name_2, bmi_2 in itertools.zip_longest(names_2, bmis_2):
    print(f"{name_2}, BMI: {bmi_2}")

