
import unittest

import numpy as np

from simulation import (
    Magnet,
    Particle,
    lorentz_acceleration,
    simulate_particle,
)


class TestParticleSimulation(unittest.TestCase):

    def test_zero_magnetic_field(self):
        """A particle should travel in a straight line with B = 0."""
        magnet = Magnet(magnetic_field_z=0.0)

        particle = Particle("test", 1.0, 1.0)

        trajectory = simulate_particle(
            particle,
            np.array([0.0, 0.0]),
            dt=0.01,
            n_steps=100,
            magnet=magnet,
        )

        np.testing.assert_allclose(
            trajectory[:, 1], 0.0, atol=1e-10
        )

        np.testing.assert_allclose(
            trajectory[:, 0],
            np.linspace(0.0, 1.0, 101),
            atol=1e-10,
        )


    def test_opposite_charges_deflect_oppositely(self):
        """Electrons and positrons should bend in opposite directions."""
        electron_acc = lorentz_acceleration(
            np.array([1.0, 0.0]), -1.0, 1.0
        )

        positron_acc = lorentz_acceleration(
            np.array([1.0, 0.0]), +1.0, 1.0
        )

        self.assertGreater(electron_acc[1], 0.0)
        self.assertLess(positron_acc[1], 0.0)


    def test_magnetic_field_preserves_speed(self):
        """A magnetic force should not change particle speed."""
        magnet = Magnet(
            x_min=-100.0,
            x_max=100.0,
            y_min=-100.0,
            y_max=100.0,
        )

        particle = Particle("test", 1.0, 1.0)

        trajectory = simulate_particle(
            particle,
            np.array([0.0, 0.0]),
            dt=0.001,
            n_steps=1000,
            magnet=magnet,
        )

        speeds = np.linalg.norm(trajectory[:, 2:], axis=1)

        np.testing.assert_allclose(speeds, 1.0, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
