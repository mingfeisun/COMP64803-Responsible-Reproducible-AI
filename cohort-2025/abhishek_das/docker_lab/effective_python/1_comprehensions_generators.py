"""
Demo 1: List Comprehensions & Generator Expressions
Goal: Show more Pythonic, efficient ways to process sequences
"""

import sys
import time


def demo_basic_comprehension():
    """Compare traditional loop vs list comprehension"""
    print("=" * 60)
    print("DEMO 1.1: Basic List Comprehension")
    print("=" * 60)
    
    squares_traditional = [] # Traditional way
    for i in range(10):
        squares_traditional.append(i ** 2)
    print(f"Traditional loop: {squares_traditional}")
    
    squares_comprehension = [i ** 2 for i in range(10)] # List comprehension (Pythonic)
    print(f"List comprehension: {squares_comprehension}")
    
    even_squares = [i ** 2 for i in range(10) if i % 2 == 0] # With filtering
    print(f"Even squares only: {even_squares}")
    print()


def demo_nested_comprehension():
    """Comprehension with nested loops"""
    print("=" * 60)
    print("DEMO 1.2: Nested Comprehensions (Matrix operations)")
    print("=" * 60)
    
    matrix = [[i + j for j in range(3)] for i in range(3)] # Create a matrix (list of lists)
    print("3x3 Matrix:")
    for row in matrix:
        print(row)
    
    flattened = [element for row in matrix for element in row] # Flatten matrix
    print(f"Flattened: {flattened}")
    print()


def demo_memory_efficiency():
    """Compare memory usage: list vs generator"""
    print("=" * 60)
    print("DEMO 1.3: Memory Efficiency - List vs Generator")
    print("=" * 60)
    
    # List comprehension - creates entire list in memory
    list_comp = [i ** 2 for i in range(1000000)]
    list_size = sys.getsizeof(list_comp)
    print(f"List comprehension size: {list_size:,} bytes")
    
    # Generator expression - lazy evaluation
    gen_exp = (i ** 2 for i in range(1000000))
    gen_size = sys.getsizeof(gen_exp)
    print(f"Generator expression size: {gen_size:,} bytes")
    print(f"Memory saved: {(list_size - gen_size) / list_size * 100:.1f}%")
    
    # Generators produce values on-demand
    print("\nFirst 5 values from generator:")
    for i, value in enumerate(gen_exp):
        if i >= 5:
            break
        print(value, end=" ")
    print("\n")


def demo_performance():
    """Performance comparison"""
    print("=" * 60)
    print("DEMO 1.4: Performance Comparison")
    print("=" * 60)
    
    n = 100000
    
    # Traditional loop
    start = time.perf_counter()
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i ** 2)
    time_loop = time.perf_counter() - start
    
    # List comprehension
    start = time.perf_counter()
    result = [i ** 2 for i in range(n) if i % 2 == 0]
    time_comp = time.perf_counter() - start
    
    print(f"Traditional loop: {time_loop:.4f} seconds")
    print(f"List comprehension: {time_comp:.4f} seconds")
    print(f"Speedup: {time_loop / time_comp:.2f}x faster")
    print()


def demo_research_example():
    """Real-world research example"""
    print("=" * 60)
    print("DEMO 1.5: Research Example - Data Filtering")
    print("=" * 60)
    
    # Simulated experimental data
    experimental_data = [
        {"id": 1, "measurement": 23.5, "quality": "good"},
        {"id": 2, "measurement": 45.2, "quality": "bad"},
        {"id": 3, "measurement": 34.1, "quality": "good"},
        {"id": 4, "measurement": 12.8, "quality": "good"},
        {"id": 5, "measurement": 56.3, "quality": "bad"},
    ]
    
    # Filter good quality measurements above threshold
    threshold = 20
    filtered_data = [
        d["measurement"] 
        for d in experimental_data 
        if d["quality"] == "good" and d["measurement"] > threshold
    ]
    
    print(f"Good quality measurements > {threshold}:")
    print(filtered_data)
    
    # Calculate statistics using generator (memory efficient for large datasets)
    mean = sum(filtered_data) / len(filtered_data)
    print(f"Mean: {mean:.2f}")
    print()


if __name__ == "__main__":
    print("\nEFFECTIVE PYTHON: COMPREHENSIONS & GENERATORS\n")
    
    demo_basic_comprehension()
    demo_nested_comprehension()
    demo_memory_efficiency()
    demo_performance()
    demo_research_example()
    
    print("=" * 60)
    print("KEY TAKEAWAYS:")
    print("List comprehensions are more Pythonic and often faster")
    print("Use generators for memory efficiency with large datasets")
    print("Perfect for data filtering and preprocessing in research")
    print("=" * 60)