# # before
# def find_even(nums):
#     for n in nums:
#         if n % 2 == 0:
#             print(f"Found even number: {n}")
#             break
#     else:
#         print("No even number found.")

# after
def find_even(nums):
    for n in nums:
        if n % 2 == 0:
            print(f"Found even number: {n}")
            return
    print("No even numbers found.")
