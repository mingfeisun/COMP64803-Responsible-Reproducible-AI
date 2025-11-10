"""
Demo 2: Context Managers (with statements)
Goal: Show proper resource management and cleanup
"""

import time
from contextlib import contextmanager
import tempfile
import os


def demo_file_handling():
    """Compare file handling with and without context manager"""
    print("=" * 60)
    print("DEMO 2.1: File Handling - The Right Way")
    print("=" * 60)
    
    # Without context manager (prone to errors)
    print("Old way (without 'with'):")
    print("   file = open('data.txt', 'w')")
    print("   file.write('data')")
    print("   file.close()  # Easy to forget!")
    print("   # If exception occurs, file may not close\n")
    
    # With context manager (automatic cleanup)
    print("Better way (with context manager):")
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    filename = temp_file.name
    temp_file.close()
    
    with open(filename, 'w') as file:
        file.write('Important research data\n')
        file.write('Automatically closed, even if error occurs!')
    
    print(f"   with open('{os.path.basename(filename)}', 'w') as file:")
    print("       file.write('data')")
    print("   # File automatically closed here!\n")
    
    # Verify file was written
    with open(filename, 'r') as file:
        content = file.read()
        print(f"File content: {content}")
    
    # Cleanup
    os.unlink(filename)
    print()


def demo_multiple_files():
    """Handle multiple resources"""
    print("=" * 60)
    print("DEMO 2.2: Multiple Resources")
    print("=" * 60)
    
    # Create temporary files
    input_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    output_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    
    input_name = input_file.name
    output_name = output_file.name
    
    # Write some data
    input_file.write("Line 1\nLine 2\nLine 3\n")
    input_file.close()
    output_file.close()
    
    # Open multiple files at once
    with open(input_name, 'r') as infile, open(output_name, 'w') as outfile:
        for line in infile:
            outfile.write(line.upper())
    
    print("Processed file (converted to uppercase):")
    with open(output_name, 'r') as f:
        print(f.read())
    
    # Cleanup
    os.unlink(input_name)
    os.unlink(output_name)
    print()


@contextmanager
def timer(label: str):
    """Custom context manager for timing code execution"""
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label}: {end - start:.4f} seconds")


def demo_custom_context_manager():
    """Create and use a custom context manager"""
    print("=" * 60)
    print("DEMO 2.3: Custom Context Manager - Timer")
    print("=" * 60)
    
    print("Timing a computation:")
    with timer("Computing sum of 1 million numbers"):
        total = sum(range(1000000))
        print(f"Result: {total:,}")
    print()
    
    print("Timing multiple operations:")
    with timer("List comprehension"):
        result = [i ** 2 for i in range(100000)]
    
    with timer("Generator expression (sum only)"):
        result = sum(i ** 2 for i in range(100000))
    print()


@contextmanager
def experiment_logger(experiment_name: str):
    """Context manager for experiment logging"""
    print(f"\n{'=' * 50}")
    print(f"Starting experiment: {experiment_name}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}")
    start_time = time.time()
    
    try:
        yield
    except Exception as e:
        print(f"\nExperiment failed: {e}")
        raise
    else:
        print(f"\nExperiment completed successfully")
    finally:
        duration = time.time() - start_time
        print(f"Duration: {duration:.2f} seconds")
        print(f"{'=' * 50}\n")


def demo_research_context_manager():
    """Research-focused context manager example"""
    print("=" * 60)
    print("DEMO 2.4: Research Example - Experiment Logger")
    print("=" * 60)
    
    with experiment_logger("Neural Network Training"):
        print("\nInitializing model...")
        time.sleep(0.5)
        
        print("Training epoch 1/3...")
        time.sleep(0.3)
        
        print("Training epoch 2/3...")
        time.sleep(0.3)
        
        print("Training epoch 3/3...")
        time.sleep(0.3)
        
        accuracy = 0.95
        print(f"\nFinal accuracy: {accuracy:.2%}")


class DatabaseConnection:
    """Simulated database connection with context manager protocol"""
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening connection to {self.db_name}...")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block (even if exception occurs)"""
        print(f"Closing connection to {self.db_name}...")
        self.connected = False
        return False  # Don't suppress exceptions
    
    def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("Not connected to database")
        return f"Results for: {sql}"


def demo_class_context_manager():
    """Context manager implemented as a class"""
    print("=" * 60)
    print("DEMO 2.5: Class-based Context Manager - Database")
    print("=" * 60)
    
    with DatabaseConnection("research_db") as db:
        result = db.query("SELECT * FROM experiments")
        print(f"Query result: {result}")
    
    print("Connection automatically closed outside 'with' block")
    print()


if __name__ == "__main__":
    print("\nEFFECTIVE PYTHON: CONTEXT MANAGERS\n")
    
    demo_file_handling()
    demo_multiple_files()
    demo_custom_context_manager()
    demo_research_context_manager()
    demo_class_context_manager()
    
    print("=" * 60)
    print("KEY TAKEAWAYS:")
    print("Always use 'with' for file operations")
    print("Context managers guarantee cleanup (even with errors)")
    print("Create custom context managers for timing, logging, resources")
    print("Use @contextmanager decorator or __enter__/__exit__ methods")
    print("=" * 60)