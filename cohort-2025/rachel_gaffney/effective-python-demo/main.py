import sys
from demos import (
    helper_functions,
    unpacking,
    exceptions,
    comprehensions,
    venv_demo,
)

DEMO_MAP = {
    "helper": helper_functions.run_demo,          # Tip 1: helper functions
    "unpack": unpacking.run_demo,                 # Tip 2: multiple assignment
    "exception": exceptions.run_demo,             # Tip 3: raise exceptions
    "comprehension": comprehensions.run_demo,     # Tip 4: comprehensions
    "model": venv_demo.run_demo,                 # Tip 5: reproducible env + final model
}

USAGE = "Usage: python main.py [helper|unpack|exception|comprehension|model|all]"

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    choice = sys.argv[1].lower()

    if choice == "all":
        for name in ["helper", "unpack", "exception", "comprehension", "model"]:
            print(f"\n=== Running demo: {name.upper()} ===")
            DEMO_MAP[name]()
        print("\n✅ All demos completed!")
        return

    func = DEMO_MAP.get(choice)
    if func is None:
        print(USAGE)
        sys.exit(1)
    func()

if __name__ == "__main__":
    main()