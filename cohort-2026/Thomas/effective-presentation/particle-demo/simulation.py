
"""
Simulate electrons and positrons travelling through a rectangular region containing a uniform magnetic field.

Units are normalised for demonstration purposes.
The simulation is non-relativistic and neglects all forces other than the magnetic Lorentz force.
"""

from dataclasses import dataclass
from time import perf_counter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numpy.typing import NDArray


Vector = NDArray[np.float64]


@dataclass
class Particle:
    """Represent a particle with a name and charge-to-mass ratio."""

    name: str
    charge_to_mass: float
    initial_speed: float


@dataclass
class Magnet:
    """Define a rectangular region with a uniform magnetic field."""

    x_min: float = 2.0
    x_max: float = 5.0
    y_min: float = -2.0
    y_max: float = 2.0
    magnetic_field_z: float = 0.1

    def contains(self, position: Vector) -> bool:
        """Return whether a position is inside the magnet."""
        x, y = position[:2]

        return ((self.x_min <= x <= self.x_max)
                and (self.y_min <= y <= self.y_max))


def lorentz_acceleration(
    velocity: Vector,
    charge_to_mass: float,
    magnetic_field_z: float,
) -> Vector:
    """Calculate acceleration due to the magnetic Lorentz force.

    The magnetic field points in the z direction, while particles
    move in the xy plane.

    Returns acceleration in the xy plane.
    """
    vx, vy = velocity

    return charge_to_mass * np.array([
        vy * magnetic_field_z,
        -vx * magnetic_field_z,
    ])


def derivatives(
    state: Vector,
    charge_to_mass: float,
    magnet: Magnet,
) -> Vector:
    """Calculate the time derivatives of position and velocity.

    State is [x, y, vx, vy].
    The magnetic field is zero outside the rectangular magnet.
    """
    position = state[:2]
    velocity = state[2:]

    if magnet.contains(position):
        acceleration = lorentz_acceleration(
            velocity,
            charge_to_mass,
            magnet.magnetic_field_z,
        )
    else:
        acceleration = np.zeros(2)

    return np.concatenate((velocity, acceleration))


def rk4_step(
    state: Vector,
    dt: float,
    charge_to_mass: float,
    magnet: Magnet,
) -> Vector:
    """Advance the particle state by one fourth-order Runge-Kutta step."""
    k1 = derivatives(state, charge_to_mass, magnet)
    k2 = derivatives(state + 0.5 * dt * k1, charge_to_mass, magnet)
    k3 = derivatives(state + 0.5 * dt * k2, charge_to_mass, magnet)
    k4 = derivatives(state + dt * k3, charge_to_mass, magnet)

    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate_particle(
    particle: Particle,
    initial_position: Vector,
    dt: float,
    n_steps: int,
    magnet: Magnet,
) -> Vector:
    """Simulate a particle trajectory using fourth-order Runge-Kutta.

    Args:
        particle: Particle properties, including charge-to-mass ratio.
        initial_position: Initial xy position.
        dt: Integration time step in simulation units.
        n_steps: Number of integration steps.
        magnet: Rectangular magnetic-field region.

    Returns:
        Array with columns [x, y, vx, vy], including the initial state.
    """
    initial_velocity = np.array([particle.initial_speed, 0.0,])

    state = np.concatenate((initial_position, initial_velocity))

    trajectory = np.zeros((n_steps + 1, 4))
    trajectory[0] = state

    for i in range(n_steps):
        state = rk4_step(state, dt, particle.charge_to_mass, magnet)
        trajectory[i + 1] = state

    return trajectory


def create_particles() -> list[Particle]:
    """Create electrons and positrons with varying initial speeds."""
    speeds = [0.8, 1.1, 1.4]

    particles = []

    for speed in speeds:
        particles.append(Particle(f"Electron (-) ({speed})", -1.0, speed))
        particles.append(Particle(f"Positron (+) ({speed})", +1.0, speed))

    return particles


def plot_trajectories(
    trajectories: dict[str, Vector],
    magnet: Magnet,
) -> None:
    """Plot all trajectories and indicate the magnet boundaries."""
    fig, ax = plt.subplots(figsize=(11, 7))

    # Draw the rectangular magnet.
    magnet_patch = Rectangle(
        (magnet.x_min, magnet.y_min),
        magnet.x_max - magnet.x_min,
        magnet.y_max - magnet.y_min,
        alpha=0.2,
        hatch="//",
        label="Magnetic field region",
    )

    ax.add_patch(magnet_patch)

    # Plot each particle trajectory.
    for name, trajectory in trajectories.items():
        x = trajectory[:, 0]
        y = trajectory[:, 1]

        ax.plot(x, y, label=name)
        ax.scatter(x[0], y[0], marker="o", s=25)

    ax.set_xlabel("x position (simulation units)", fontsize=18)
    ax.set_ylabel("y position (simulation units)", fontsize=18)
    ax.set_title("Electron and positron trajectories in a magnetic field", fontsize=20)

    ax.axhline(0, linewidth=0.5, alpha=0.5)
    ax.axvline(0, linewidth=0.5, alpha=0.5)

    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=12, loc="upper right")

    plt.tight_layout()
    plt.savefig("trajectories.png", dpi=200)
    print("Saved plot to trajectories.png")


def main() -> None:
    """Run the particle simulation and measure its execution time."""
    magnet = Magnet()
    particles = create_particles()

    initial_position = np.array([0.0, 0.0])

    dt = 0.005
    n_steps = 1500

    trajectories = {}

    # Measure the time taken to simulate all particles.
    start_time = perf_counter()

    for particle in particles:
        trajectories[particle.name] = simulate_particle(
            particle=particle,
            initial_position=initial_position,
            dt=dt,
            n_steps=n_steps,
            magnet=magnet,
        )

    elapsed = perf_counter() - start_time

    print(f"Simulated {len(particles)} particles")
    print(f"Simulation time: {elapsed:.4f} seconds")

    plot_trajectories(trajectories, magnet)


if __name__ == "__main__":
    main()
