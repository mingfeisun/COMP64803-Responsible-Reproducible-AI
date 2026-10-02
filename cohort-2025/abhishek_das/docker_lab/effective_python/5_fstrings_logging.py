"""
Demo 5: F-strings & Logging
Goal: Show modern string formatting and proper logging practices
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def demo_fstring_basics():
    """Basic f-string usage"""
    print("=" * 60)
    print("DEMO 5.1: F-string Basics")
    print("=" * 60)
    
    name = "Neural Network"
    accuracy = 0.9567
    epochs = 100
    
    # Old ways (less readable)
    print("Old ways:")
    print("  % formatting: 'Model: %s, Accuracy: %.2f%%' % (name, accuracy * 100)")
    print("  .format(): 'Model: {}, Accuracy: {:.2f}%'.format(name, accuracy * 100)")
    print()
    
    # F-strings (modern, readable, fast)
    print("F-string (modern):")
    result = f"Model: {name}, Accuracy: {accuracy:.2%}, Epochs: {epochs}"
    print(f"  {result}")
    print()


def demo_fstring_expressions():
    """F-strings with expressions and formatting"""
    print("=" * 60)
    print("DEMO 5.2: F-strings with Expressions")
    print("=" * 60)
    
    # Expressions inside f-strings
    x, y = 10, 20
    print(f"Sum of {x} and {y} is {x + y}")
    print(f"Product: {x * y}")
    print()
    
    # Formatting numbers
    value = 1234.56789
    print("Number formatting:")
    print(f"  Raw: {value}")
    print(f"  2 decimals: {value:.2f}")
    print(f"  With commas: {value:,.2f}")
    print(f"  Scientific: {value:.2e}")
    print(f"  Percentage: {0.8567:.2%}")
    print()
    
    # Dates
    now = datetime.now()
    print("Date formatting:")
    print(f"  ISO format: {now:%Y-%m-%d %H:%M:%S}")
    print(f"  Custom: {now:%B %d, %Y at %I:%M %p}")
    print()


def demo_fstring_alignment():
    """F-string alignment and padding"""
    print("=" * 60)
    print("DEMO 5.3: Alignment and Padding")
    print("=" * 60)
    
    # Table formatting
    print("Experiment Results Table:")
    print(f"{'ID':<5} {'Model':<15} {'Accuracy':>10} {'Loss':>8}")
    print("-" * 40)
    
    results = [
        (1, "ResNet", 0.9234, 0.0876),
        (2, "VGG", 0.8967, 0.1234),
        (3, "MobileNet", 0.9156, 0.0945),
    ]
    
    for exp_id, model, acc, loss in results:
        print(f"{exp_id:<5} {model:<15} {acc:>10.2%} {loss:>8.4f}")
    print()


def demo_fstring_debugging():
    """F-string debugging feature (Python 3.8+)"""
    print("=" * 60)
    print("DEMO 5.4: F-string Debugging (Python 3.8+)")
    print("=" * 60)
    
    learning_rate = 0.001
    batch_size = 32
    epochs = 100
    
    # Debug notation: shows variable name and value
    print("Quick debugging with f-string:")
    print(f"{learning_rate=}")
    print(f"{batch_size=}")
    print(f"{epochs=}")
    print()
    
    # Can combine with formatting
    accuracy = 0.95678
    print(f"{accuracy=:.2%}")
    print()


def demo_multiline_fstrings():
    """Multi-line f-strings for reports"""
    print("=" * 60)
    print("DEMO 5.5: Multi-line F-strings for Reports")
    print("=" * 60)
    
    exp_name = "Deep Learning Experiment #42"
    model = "ResNet-50"
    accuracy = 0.9567
    precision = 0.9423
    recall = 0.9612
    f1_score = 0.9516
    
    report = f"""
    Experiment Report
    {'=' * 40}
    Name: {exp_name}
    Model: {model}
    
    Performance Metrics:
    - Accuracy:  {accuracy:.2%}
    - Precision: {precision:.2%}
    - Recall:    {recall:.2%}
    - F1 Score:  {f1_score:.2%}
    
    Status: {'SUCCESS' if accuracy > 0.95 else ' NEEDS IMPROVEMENT'}
    """
    
    print(report)


def setup_logging_basic():
    """Basic logging setup"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def demo_logging_basics():
    """Basic logging levels and usage"""
    print("=" * 60)
    print("DEMO 5.6: Logging Basics")
    print("=" * 60)
    
    # Create logger
    logger = logging.getLogger("ExperimentLogger")
    logger.setLevel(logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    print("\nLogging at different levels:\n")
    
    # Different log levels
    logger.debug("Debug message: Loading configuration...")
    logger.info("Info message: Starting training...")
    logger.warning("Warning message: Learning rate is high!")
    logger.error("Error message: Failed to load checkpoint!")
    logger.critical("Critical message: Out of memory!")
    
    print()
    
    # Clear handlers for next demo
    logger.handlers.clear()


def demo_logging_vs_print():
    """Why logging is better than print"""
    print("=" * 60)
    print("DEMO 5.7: Logging vs Print Statements")
    print("=" * 60)
    
    print("\n Using print (problems):")
    print("  - Always outputs (can't disable easily)")
    print("  - Goes to stdout (mixed with actual output)")
    print("  - No severity levels")
    print("  - No timestamps or metadata")
    print("  - Can't redirect to files easily")
    print()
    
    print(" Using logging (benefits):")
    print("  - Can enable/disable by level")
    print("  - Can output to multiple destinations")
    print("  - Has severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    print("  - Includes timestamps and context")
    print("  - Can filter by module or component")
    print()


def demo_logging_to_file():
    """Logging to both console and file"""
    print("=" * 60)
    print("DEMO 5.8: Logging to File and Console")
    print("=" * 60)
    
    # Create logger
    logger = logging.getLogger("FileLogger")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # Console handler (INFO and above)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(console_formatter)
    
    # File handler (DEBUG and above)
    log_file = Path("experiment.log")  # Use current directory
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    print("\nLogging to both console and file:\n")
    
    logger.debug("This goes to file only (not console)")
    logger.info("This goes to both file and console")
    logger.warning("Warning in both places")
    logger.error("Error logged everywhere")
    
    print(f"\nLog file created at: {log_file}")
    print("\nLog file contents:")
    print("-" * 40)
    with open(log_file, 'r') as f:
        print(f.read())
    
    # Cleanup
    logger.handlers.clear()
    log_file.unlink()
    print()


def demo_research_example():
    """Complete research example with f-strings and logging"""
    print("=" * 60)
    print("DEMO 5.9: Research Example - Experiment Tracking")
    print("=" * 60)
    
    # Setup logger
    logger = logging.getLogger("ResearchLogger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                   datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    print("\nSimulating experiment:\n")
    
    # Experiment parameters
    experiment_id = 42
    model_name = "ResNet-50"
    learning_rate = 0.001
    batch_size = 32
    
    logger.info(f"Starting Experiment #{experiment_id}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Learning rate: {learning_rate}, Batch size: {batch_size}")
    
    # Simulate training
    for epoch in range(1, 4):
        train_loss = 0.5 / epoch
        val_loss = 0.6 / epoch
        accuracy = 0.7 + (epoch * 0.08)
        
        logger.info(
            f"Epoch {epoch}/3 - "
            f"Train Loss: {train_loss:.4f}, "
            f"Val Loss: {val_loss:.4f}, "
            f"Accuracy: {accuracy:.2%}"
        )
    
    final_accuracy = 0.9456
    
    if final_accuracy > 0.90:
        logger.info(f"SUCCESS: Final accuracy {final_accuracy:.2%}")
    else:
        logger.warning(f"Accuracy {final_accuracy:.2%} below target")
    
    logger.info("Experiment complete!")
    
    # Generate summary with f-string
    summary = f"""
    {'=' * 50}
    Experiment #{experiment_id} Summary
    {'=' * 50}
    Model: {model_name}
    Final Accuracy: {final_accuracy:.2%}
    Status: {'PASSED' if final_accuracy > 0.90 else 'FAILED'}
    {'=' * 50}
    """
    
    print(summary)
    
    logger.handlers.clear()


if __name__ == "__main__":
    print("\nEFFECTIVE PYTHON: F-STRINGS & LOGGING\n")
    
    demo_fstring_basics()
    demo_fstring_expressions()
    demo_fstring_alignment()
    demo_fstring_debugging()
    demo_multiline_fstrings()
    demo_logging_basics()
    demo_logging_vs_print()
    demo_logging_to_file()
    demo_research_example()
    
    print("=" * 60)
    print("KEY TAKEAWAYS:")
    print("F-strings: fast, readable, support expressions and formatting")
    print("Use f'{variable=}' for quick debugging")
    print("Logging > print: levels, filtering, multiple outputs")
    print("Log to both console and files for experiment tracking")
    print("Essential for research: reproducibility and debugging")
    print("=" * 60)