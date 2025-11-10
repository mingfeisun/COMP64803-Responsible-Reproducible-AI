class Demo1:
    def __init__(self):
        print("In Demo1, the method careful_divide can return None")
        self.main_demo()
    
    def careful_divide(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return None
        
    def careful_divide2(self, a, b):
        try:
            return True, a / b
        except ZeroDivisionError:
            return False, None

    def main_demo(self):
        
        x, y = 1, 0
        result = self.careful_divide(x, y)
        
        if result is None:
            print(f"Invalid Inputs! {x} / {y}")

        # So far this seems fine, let's see a different case
        x, y = 0, 5
        result = self.careful_divide(x, y)

        if not result:
            print(f"Invalid Inputs! {x} / {y}")
        
        _, result = self.careful_divide2(x, y)
        
        # relies on us still unpacking the value
        if not result:
            print(f"Invalid Inputs! {x} / {y}")


class Demo2:
    def __init__(self):
        print("In Demo2, we show 'good' practice and raise an Exception instead!")
        self.main_demo()
    
    def careful_divide(self, a, b):
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError("ValueError: Zero Division!")
        

    def main_demo(self):
        
        x, y = 1, 0

        try:
            result = self.careful_divide(x, y)
        except ValueError:
            print(f"Invalid Inputs! {x} / {y}")
        else:
            print("Result is %.1f" % result)


if __name__ == "__main__":

    demo1 = Demo1()
    demo2 = Demo2()

