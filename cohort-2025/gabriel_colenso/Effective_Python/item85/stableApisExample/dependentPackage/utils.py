from . objects import Particle   

__all__ = ['new_position']

def step_forward(Particle, dt):
    return Particle.velocity_u*dt, Particle.velocity_v*dt

def new_position(Particle, dt):
    dx, dy = step_forward(Particle, dt)
    return Particle.position[0] + dx, Particle.position[1] + dy