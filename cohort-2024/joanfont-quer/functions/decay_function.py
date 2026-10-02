"""

Defines the Bateman equation.

"""
import numpy as np


def decay_function(t, decay_rb, decay_sr):
    """
    Caclulates the percentage of activity at a specific time.
    :param t: float, ndarray of floats
    :param decay_rb: float
    :param decay_sr: float
    :return: float, ndarray of floats
    """
    if abs(decay_rb - decay_sr) < 0.0000001:
        decay_sr += 0.0000001
    activity = ((decay_rb * decay_sr) / (decay_rb - decay_sr)) * \
               (np.exp(-decay_sr * t) - np.exp(-decay_rb * t))
    return activity
