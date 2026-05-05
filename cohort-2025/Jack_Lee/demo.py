import numpy as np
import time

def loop_sum(data):
    total = 0
    for x in data:
        total += x
    return total

def vector_sum(data):
    return np.sum(data)


def vectorisation():
    """time vectorised vs not vecotrised sum"""

    data = np.random.rand(1_000_000)

    start_time = time.time()
    loop_result = loop_sum(data)
    end_time = time.time()
    print(f"Loop sum: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    vector_result = vector_sum(data)
    end_time = time.time()
    print(f"Vector sum: {end_time - start_time:.4f} seconds")



def comprehension():
    l=range(10)
    
    squaresl= map(lambda x: x ** 2, l)

    squares = [x**2 for x in l]

    print(squares)


class Furniture():
    """any furniture"""

    def __init__(self, mass):

        self.__mass=mass

    @property
    def mass(self):
        """gets the mass without letting you change it"""
        return self.__mass

class Chair(Furniture):
    """a chair"""
    
    def __init__(self, mass,legs):
        
        super().__init__(mass)
        
        self.legs=legs


if __name__ == "__main__":
    vectorisation()


    comprehension()
    

    stool=Chair(10,3)

    print(stool._Furniture__mass)

    print(stool.mass)

    try:
        stool.mass=5
        print(stool.mass)
    except(AttributeError):
        print("can't change mass through property decorator")
