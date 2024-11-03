import time 
import traceback 
import sys 

# A context manager class must have an enter and exit method defined
class Timer():
    # Here we use __enter__ to describe the behaviour that occurs when the timer
    # is instatiated, this will be called by the "with" function
    def __enter__(self):
        self.start_time = time.time() 

    # The __exit__ method is called in the 'finally' part of the try / finally 
    # block of the with function. If an error occurs, three arguments are passed
    # the three arguments are the exception type, exception value, and the traceback
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.end_time = time.time() 
        self.elapsed = self.end_time - self.start_time 
        print(f"Elapsed time {self.elapsed:.4f} seconds")
        
        if exc_type: 
            print('Exception has occured')
            print(f'Type {exc_type}')
            print(f'Value {exc_value}')
            print(f'Traceback')
            traceback.print_tb(exc_traceback)
            return True  

def experiment(): 
    with Timer() as timer: 
        for x in range(100000):
            pass 

    # with Timer() as timer: 
    #     for x in range(100000):
    #         if x < 90000: 
    #             pass
    #         else: 
    #             x / 0 

    # # This is semantically equivalent to doing the following code block

    # manager = Timer
    # enter = manager.__enter__
    # exit = manager.__exit__ 
    # hit_except = False 

    # try: 
    #     TARGET = enter(manager)
    #     for x in range(100000): 
    #         pass 
    # except: 
    #     hit_except = True 
    #     if not exit(manager, *sys.exc_info()):
    #         raise 
    # finally: 
    #     if not hit_except: 
    #         exit(manager, None, None, None)


if __name__ == "__main__":
    experiment()