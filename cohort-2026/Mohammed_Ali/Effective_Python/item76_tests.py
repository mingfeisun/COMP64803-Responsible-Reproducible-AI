"""Item 76: Verify related behaviors in TestCase subclasses.

Tests that a Lennard-Jones energy and force calculation obeys physics.
A base class holds the shared setup and a helper; the test classes that
inherit from it each check one group of related behaviours.

Run: python item76_tests.py
"""
import unittest

import numpy as np


def lj_energy(pos):
    """Total Lennard-Jones energy of a cluster of atoms."""
    diff = pos[:, None, :] - pos[None, :, :]
    r = np.sqrt((diff**2).sum(axis=2))
    i, j = np.triu_indices(len(pos), k=1)  # every pair once
    r = r[i, j]
    return np.sum(4 * (r**-12 - r**-6))


def lj_forces(pos):
    """Force on each atom, from the derivative of the formula above."""
    diff = pos[:, None, :] - pos[None, :, :]
    r2 = (diff**2).sum(axis=2)
    np.fill_diagonal(r2, np.inf)  # an atom exerts no force on itself
    strength = 24 * (2 * r2**-7 - r2**-4)
    return (strength[:, :, None] * diff).sum(axis=1)


def random_rotation(rng):
    """A random 3x3 rotation matrix."""
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q * np.sign(np.diag(r))
    if np.linalg.det(q) < 0:
        q[:, 0] = -q[:, 0]
    return q


class PhysicsTestCase(unittest.TestCase):
    """Shared setup and helper. Holds no tests itself."""

    def setUp(self):
        # 27 atoms on a slightly wobbly 3 x 3 x 3 grid
        self.rng = np.random.default_rng(0)
        grid = np.array([[i, j, k] for i in range(3) for j in range(3) for k in range(3)], float)
        self.pos = 1.12 * grid + self.rng.normal(scale=0.05, size=grid.shape)

    def assertSameEnergy(self, pos_a, pos_b):
        self.assertAlmostEqual(lj_energy(pos_a), lj_energy(pos_b), places=9)


class SymmetryTests(PhysicsTestCase):
    """Moving, turning or renumbering the atoms must not change the energy."""

    def test_translation(self):
        self.assertSameEnergy(self.pos, self.pos + [3.0, -1.0, 2.0])

    def test_rotation(self):
        for k in range(5):
            with self.subTest(rotation=k):  # reports each rotation separately
                R = random_rotation(self.rng)
                self.assertSameEnergy(self.pos, self.pos @ R.T)

    def test_renumbering(self):
        shuffled = self.pos[self.rng.permutation(len(self.pos))]
        self.assertSameEnergy(self.pos, shuffled)


class ForceTests(PhysicsTestCase):
    """Forces must agree with the energy."""

    def test_force_is_minus_energy_slope(self):
        forces = lj_forces(self.pos)
        h = 1e-6
        for atom in [0, 13, 26]:
            for axis in range(3):
                with self.subTest(atom=atom, axis=axis):
                    plus, minus = self.pos.copy(), self.pos.copy()
                    plus[atom, axis] += h
                    minus[atom, axis] -= h
                    slope = (lj_energy(plus) - lj_energy(minus)) / (2 * h)
                    self.assertAlmostEqual(forces[atom, axis], -slope, delta=1e-4)

    def test_forces_add_up_to_zero(self):
        # Newton's third law: every push has an equal and opposite push
        total = lj_forces(self.pos).sum(axis=0)
        np.testing.assert_allclose(total, 0, atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
