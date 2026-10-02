import json
import torch

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


@torch.autocast("cuda", enabled=False)
def partial_forward(model, x):
    return model(x)


def some_code():
    pass

import logging

class debug_logging:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger()
        self.old_level = self.logger.level

    def __enter__(self):
        self.logger.setLevel(logging.DEBUG)
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.setLevel(self.old_level)

logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

with debug_logging(logger):
    some_code()
    