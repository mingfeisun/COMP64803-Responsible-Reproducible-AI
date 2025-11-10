__all__ = ['Particle']


class Particle:
    def __init__(self, position, velocity_u, velocity_v):
        self.position = position
        self.velocity_u = velocity_u
        self.velocity_v = velocity_v