from dataclasses import dataclass, field
from typing import Literal, List

@dataclass(frozen=True, slots=True)
class TrainingConfig:
    batch_size: int
    learning_rate: float
    num_epochs: int
    
    model_name: Literal["vit_small", "vit_base", "vit_large"]
    optimizer: Literal["adamw", "sgd"]
    
    augmentations: List[str] = field(default_factory=list)
    device: Literal["cpu", "cuda"] = "cuda"
    
    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive.")
        if not (0 < self.learning_rate <= 1):
            raise ValueError("learning_rate must be in range (0, 1].")
        if self.num_epochs <= 0:
            raise ValueError("num_epochs must be positive.")
