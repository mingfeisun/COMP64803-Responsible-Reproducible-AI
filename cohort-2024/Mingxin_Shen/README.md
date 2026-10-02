# 5 Effective Way in Python

build the image and run from them

```bash
docker build -t pres .
docker run -it pres
```

- item 19: Never Unpack More Than Three Variables When Functions Return Multiple Values
    - easy to confuse when unpacking, especially when they're of the same data type
    - use dictionary or named tuple instead
- item 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments
    - keyword argument can be specified directly as position argument without enforcemnet
    - could lead to misplaced arguments
- item 75: Use repr Strings for Debugging Output
    - string of a number cannot be tell when printed
    * (what's the purpose of repr? other repr differ from print example?)
- item 76: Verify Related Behaviors in TestCase Subclasses
- item 80: Consider Interactive Debugging with pdb
    - place a breakpoint in the script to evaluate variables in the middle of execution
    - call the breakpoint() as a function

```bash
python -m unittest test_item7680.py
```