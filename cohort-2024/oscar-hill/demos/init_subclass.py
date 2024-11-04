class Item:
    age = 0

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.age < 0:
            raise ValueError("age must be greater than 0.")
        
class Table(Item):
    age = -1
