from dataclasses import dataclass

person_dict = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

print(person_dict["name"]) 
print(person_dict["age"])  

# But easy to make mistakes:
person_dict["agge"] = 31
print(person_dict)



@dataclass
class Person:
    name: str
    age: int
    email: str

person_dc = Person(name="Alice", age=30, email="alice@example.com")

# Accessing data
print(person_dc.name)
print(person_dc.age) 

