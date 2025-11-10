"""
Demo 3: Type Hints & Data Validation
Goal: Show how type hints make code more maintainable and catch bugs
"""

from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator, ValidationError


def demo_basic_type_hints():
    """Basic type hints for function parameters and return values"""
    print("=" * 60)
    print("DEMO 3.1: Basic Type Hints")
    print("=" * 60)
    
    # Without type hints (unclear what types are expected)
    def calculate_stats_old(data):
        return sum(data) / len(data), max(data), min(data)
    
    # With type hints (self-documenting)
    def calculate_stats(data: List[float]) -> Tuple[float, float, float]:
        """Calculate mean, max, min of numeric data."""
        mean = sum(data) / len(data)
        maximum = max(data)
        minimum = min(data)
        return mean, maximum, minimum
    
    print("Function signature with type hints:")
    print("def calculate_stats(data: List[float]) -> Tuple[float, float, float]:")
    print("    ...")
    print()
    
    sample_data = [23.5, 45.2, 34.1, 12.8, 56.3]
    mean, maximum, minimum = calculate_stats(sample_data)
    
    print(f"Data: {sample_data}")
    print(f"Mean: {mean:.2f}, Max: {maximum:.2f}, Min: {minimum:.2f}")
    print()


def demo_optional_union():
    """Optional and Union types"""
    print("=" * 60)
    print("DEMO 3.2: Optional and Union Types")
    print("=" * 60)
    
    def find_participant(
        participant_id: int, 
        participants: List[Dict[str, Union[int, str]]]
    ) -> Optional[Dict[str, Union[int, str]]]:
        """
        Find a participant by ID.
        Returns None if not found.
        """
        for participant in participants:
            if participant.get("id") == participant_id:
                return participant
        return None
    
    participants = [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "Bob", "age": 30},
        {"id": 3, "name": "Charlie", "age": 35},
    ]
    
    print("Finding participant with ID 2:")
    result = find_participant(2, participants)
    print(f"Result: {result}")
    
    print("\nFinding non-existent participant:")
    result = find_participant(99, participants)
    print(f"Result: {result} (None indicates not found)")
    print()


@dataclass
class ExperimentResult:
    """Using dataclass with type hints"""
    experiment_id: int
    accuracy: float
    loss: float
    epochs: int
    notes: Optional[str] = None
    
    def is_successful(self) -> bool:
        """Check if experiment met success criteria"""
        return self.accuracy > 0.90 and self.loss < 0.1


def demo_dataclass():
    """Dataclasses for structured data"""
    print("=" * 60)
    print("DEMO 3.3: Dataclasses with Type Hints")
    print("=" * 60)
    
    # Create experiment result
    result = ExperimentResult(
        experiment_id=101,
        accuracy=0.95,
        loss=0.05,
        epochs=50,
        notes="Used Adam optimizer"
    )
    
    print(f"Experiment #{result.experiment_id}")
    print(f"Accuracy: {result.accuracy:.2%}")
    print(f"Loss: {result.loss:.3f}")
    print(f"Epochs: {result.epochs}")
    print(f"Success: {result.is_successful()}")
    print()


class ExperimentConfig(BaseModel):
    """Pydantic model for runtime validation"""
    name: str = Field(..., min_length=1, max_length=100)
    learning_rate: float = Field(gt=0, le=1)  # 0 < lr <= 1
    batch_size: int = Field(ge=1, le=1024)  # 1 <= bs <= 1024
    epochs: int = Field(ge=1)
    use_gpu: bool = True
    random_seed: Optional[int] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip()
    
    @validator('learning_rate')
    def learning_rate_reasonable(cls, v):
        if v > 0.1:
            print(f"Warning: Learning rate {v} is quite high!")
        return v


def demo_pydantic_validation():
    """Pydantic for data validation"""
    print("=" * 60)
    print("DEMO 3.4: Pydantic Data Validation")
    print("=" * 60)
    
    # Valid configuration
    print("Creating valid configuration:")
    try:
        config = ExperimentConfig(
            name="ResNet Training",
            learning_rate=0.001,
            batch_size=32,
            epochs=100,
            random_seed=42
        )
        print(f"   Config created successfully:")
        print(f"   Name: {config.name}")
        print(f"   Learning rate: {config.learning_rate}")
        print(f"   Batch size: {config.batch_size}")
        print()
    except ValidationError as e:
        print(f"Validation failed: {e}")
    
    # Invalid configuration (negative learning rate)
    print("Attempting invalid configuration (negative learning rate):")
    try:
        bad_config = ExperimentConfig(
            name="Bad Config",
            learning_rate=-0.01,  # Invalid!
            batch_size=32,
            epochs=100
        )
    except ValidationError as e:
        print(f"Validation caught error:")
        for error in e.errors():
            print(f"   Field: {error['loc'][0]}")
            print(f"   Error: {error['msg']}")
    print()
    
    # Invalid configuration (batch size too large)
    print("Attempting invalid configuration (batch size too large):")
    try:
        bad_config = ExperimentConfig(
            name="Bad Config",
            learning_rate=0.001,
            batch_size=2048,  # Too large!
            epochs=100
        )
    except ValidationError as e:
        print(f"Validation caught error:")
        for error in e.errors():
            print(f"   Field: {error['loc'][0]}")
            print(f"   Error: {error['msg']}")
    print()


def process_measurements(
    data: List[float],
    threshold: Optional[float] = None,
    normalize: bool = False
) -> List[float]:
    """
    Process measurement data with optional filtering and normalization.
    
    Args:
        data: List of measurement values
        threshold: Optional minimum value to keep
        normalize: Whether to normalize to [0, 1] range
    
    Returns:
        Processed measurement data
    """
    result = data.copy()
    
    # Filter by threshold
    if threshold is not None:
        result = [x for x in result if x >= threshold]
    
    # Normalize
    if normalize and result:
        min_val = min(result)
        max_val = max(result)
        if max_val > min_val:
            result = [(x - min_val) / (max_val - min_val) for x in result]
    
    return result


def demo_research_example():
    """Complete research example with type hints"""
    print("=" * 60)
    print("DEMO 3.5: Research Example - Data Processing Pipeline")
    print("=" * 60)
    
    raw_data = [12.5, 45.2, 8.3, 34.1, 67.8, 23.4, 5.6]
    
    print(f"Raw data: {raw_data}")
    
    # Filter and normalize
    processed = process_measurements(
        data=raw_data,
        threshold=10.0,
        normalize=True
    )
    
    print(f"Filtered (>= 10) and normalized: {[f'{x:.3f}' for x in processed]}")
    print()


if __name__ == "__main__":
    print("\nEFFECTIVE PYTHON: TYPE HINTS & VALIDATION\n")
    
    demo_basic_type_hints()
    demo_optional_union()
    demo_dataclass()
    demo_pydantic_validation()
    demo_research_example()
    
    print("=" * 60)
    print("KEY TAKEAWAYS:")
    print("Type hints make code self-documenting")
    print("IDEs can provide better autocomplete and catch errors early")
    print("Dataclasses reduce boilerplate for data structures")
    print("Pydantic provides runtime validation for external data")
    print("Critical for research code: prevents bugs in data processing")
    print("=" * 60)