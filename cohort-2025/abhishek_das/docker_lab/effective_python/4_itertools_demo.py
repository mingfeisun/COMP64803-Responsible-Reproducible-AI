"""
Demo 4: Efficient Data Processing with itertools
Goal: Show memory-efficient iteration tools for data processing
"""

import itertools
from typing import List, Iterator


def demo_groupby():
    """Group consecutive items by key"""
    print("=" * 60)
    print("DEMO 4.1: itertools.groupby - Group Sequential Data")
    print("=" * 60)
    
    # Research data: measurements with quality labels
    data = [
        ("A", 23.5), ("A", 25.1), ("A", 24.8),  # Group 1
        ("B", 45.2), ("B", 46.3),                # Group 2
        ("A", 22.1), ("A", 23.9),                # Group 3
        ("C", 67.8), ("C", 68.2), ("C", 66.9),  # Group 4
    ]
    
    print("Original data (condition, measurement):")
    for item in data:
        print(f"  {item}")
    print()
    
    # Group by first element (condition)
    print("Grouped by condition:")
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        measurements = [item[1] for item in group]
        avg = sum(measurements) / len(measurements)
        print(f"  Condition {key}: {measurements} (avg: {avg:.2f})")
    print()


def demo_combinations_permutations():
    """Generate combinations and permutations"""
    print("=" * 60)
    print("DEMO 4.2: Combinations & Permutations")
    print("=" * 60)
    
    # Experimental conditions
    conditions = ["Control", "Treatment_A", "Treatment_B"]
    
    # All pairwise comparisons (combinations)
    print("All pairwise comparisons:")
    for pair in itertools.combinations(conditions, 2):
        print(f"  Compare {pair[0]} vs {pair[1]}")
    print()
    
    # Different orderings (permutations)
    print("All possible orderings (first 3):")
    for i, perm in enumerate(itertools.permutations(conditions), 1):
        print(f"  Order {i}: {' -> '.join(perm)}")
        if i >= 3:
            break
    print()
    
    # Combinations with replacement (selecting with repetition)
    print("Sampling with replacement (2 items):")
    for combo in itertools.combinations_with_replacement(["A", "B"], 2):
        print(f"  {combo}")
    print()


def demo_chain():
    """Chain multiple iterables together"""
    print("=" * 60)
    print("DEMO 4.3: itertools.chain - Combine Multiple Datasets")
    print("=" * 60)
    
    # Data from multiple experiments
    experiment_1 = [12.5, 13.2, 14.1]
    experiment_2 = [23.4, 24.1, 22.8]
    experiment_3 = [45.6, 46.2, 44.9]
    
    print("Individual experiments:")
    print(f"  Exp 1: {experiment_1}")
    print(f"  Exp 2: {experiment_2}")
    print(f"  Exp 3: {experiment_3}")
    print()
    
    # Combine all data efficiently (no intermediate list)
    all_data = itertools.chain(experiment_1, experiment_2, experiment_3)
    
    print("Combined data:")
    print(f"  {list(all_data)}")
    print()


def demo_islice():
    """Slice iterators efficiently"""
    print("=" * 60)
    print("DEMO 4.4: itertools.islice - Efficient Slicing")
    print("=" * 60)
    
    # Large data stream (simulated)
    def data_stream():
        """Generator simulating a large data source"""
        for i in range(1000000):
            yield i ** 2
    
    print("Getting first 5 items from large data stream:")
    first_five = list(itertools.islice(data_stream(), 5))
    print(f"  {first_five}")
    
    print("\nGetting items 10-15 from data stream:")
    items_10_to_15 = list(itertools.islice(data_stream(), 10, 15))
    print(f"  {items_10_to_15}")
    
    print("\nMemory efficient! (Doesn't load all 1M items)")
    print()


def demo_accumulate():
    """Running totals and reductions"""
    print("=" * 60)
    print("DEMO 4.5: itertools.accumulate - Running Statistics")
    print("=" * 60)
    
    daily_measurements = [12, 15, 13, 18, 20, 17, 19]
    
    print(f"Daily measurements: {daily_measurements}")
    
    # Running sum
    running_sum = list(itertools.accumulate(daily_measurements))
    print(f"Running sum: {running_sum}")
    
    # Running maximum
    import operator
    running_max = list(itertools.accumulate(daily_measurements, max))
    print(f"Running max: {running_max}")
    
    # Running average (custom function)
    def running_average(accumulated, new_value):
        if isinstance(accumulated, tuple):
            total, count = accumulated
        else:
            total, count = accumulated, 1
        return (total + new_value, count + 1)
    
    print()


def demo_product():
    """Cartesian product of iterables"""
    print("=" * 60)
    print("DEMO 4.6: itertools.product - Experimental Design")
    print("=" * 60)
    
    # Experimental factors
    temperatures = [20, 25, 30]
    ph_levels = [6.5, 7.0, 7.5]
    
    print("Temperature options:", temperatures)
    print("pH options:", ph_levels)
    print()
    
    print("All experimental conditions (factorial design):")
    for temp, ph in itertools.product(temperatures, ph_levels):
        print(f"  Temperature: {temp}°C, pH: {ph}")
    
    total = len(temperatures) * len(ph_levels)
    print(f"\nTotal conditions: {total}")
    print()


def demo_cycle_repeat():
    """Cycle and repeat iterables"""
    print("=" * 60)
    print("DEMO 4.7: itertools.cycle & repeat - Infinite Iterators")
    print("=" * 60)
    
    # Cycle through conditions
    conditions = ["Control", "Treatment"]
    
    print("Assigning participants to conditions (alternating):")
    participants = ["P1", "P2", "P3", "P4", "P5", "P6"]
    
    for participant, condition in zip(participants, itertools.cycle(conditions)):
        print(f"  {participant} -> {condition}")
    print()
    
    # Repeat a value
    print("Creating control group (5 participants):")
    control_assignments = list(zip(
        ["P1", "P2", "P3", "P4", "P5"],
        itertools.repeat("Control", 5)
    ))
    for assignment in control_assignments:
        print(f"  {assignment[0]} -> {assignment[1]}")
    print()


def batch_processor(data: Iterator, batch_size: int):
    """Process data in batches (research pipeline example)"""
    iterator = iter(data)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def demo_research_pipeline():
    """Complete research example using multiple itertools"""
    print("=" * 60)
    print("DEMO 4.8: Research Example - Data Processing Pipeline")
    print("=" * 60)
    
    # Simulated large dataset
    def generate_measurements():
        """Simulate reading from a large data source"""
        for i in range(50):
            yield {"id": i, "value": (i % 10) + 10 + (i * 0.1)}
    
    print("Processing large dataset in batches of 10:")
    
    # Process in batches
    batch_num = 0
    for batch in batch_processor(generate_measurements(), batch_size=10):
        batch_num += 1
        values = [item["value"] for item in batch]
        avg = sum(values) / len(values)
        print(f"  Batch {batch_num}: avg = {avg:.2f} ({len(batch)} items)")
        
        if batch_num >= 3:  # Just show first 3 batches for demo
            print("  ...")
            break
    
    print("\nMemory efficient: Only 10 items in memory at a time!")
    print()


def demo_filterfalse():
    """Filter out items that don't meet criteria"""
    print("=" * 60)
    print("DEMO 4.9: itertools.filterfalse - Remove Invalid Data")
    print("=" * 60)
    
    measurements = [
        {"id": 1, "value": 23.5, "valid": True},
        {"id": 2, "value": None, "valid": False},
        {"id": 3, "value": 34.1, "valid": True},
        {"id": 4, "value": 12.8, "valid": False},
        {"id": 5, "value": 45.2, "valid": True},
    ]
    
    print("Original measurements:")
    for m in measurements:
        print(f"  {m}")
    print()
    
    # Remove invalid measurements
    valid_measurements = itertools.filterfalse(
        lambda x: not x["valid"],
        measurements
    )
    
    print("Valid measurements only:")
    for m in valid_measurements:
        print(f"  {m}")
    print()


if __name__ == "__main__":
    print("\nEFFECTIVE PYTHON: ITERTOOLS FOR EFFICIENT DATA PROCESSING\n")
    
    demo_groupby()
    demo_combinations_permutations()
    demo_chain()
    demo_islice()
    demo_accumulate()
    demo_product()
    demo_cycle_repeat()
    demo_research_pipeline()
    demo_filterfalse()
    
    print("=" * 60)
    print("KEY TAKEAWAYS:")
    print("itertools provides memory-efficient iterator operations")
    print("Perfect for large datasets that don't fit in memory")
    print("Combinatorial tools: combinations, permutations, product")
    print("Data processing: groupby, chain, accumulate")
    print("Essential for research: experimental design, batch processing")
    print("=" * 60)