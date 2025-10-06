"""

Defines a loss function.

"""
import numpy as np
from functions.decay_function import decay_function as function


def objective_fixed(theta, t, y):
    """
    Mean sauared error.
    :param theta: ndarray of floats
    :param t: ndarray of floats
    :param y: ndarray of floats
    :return: float
    """
    if abs(theta[0] - theta[1]) < 0.0000001:
        theta[1] += 0.0000001

    y_pred = function(t, theta[0], theta[1])
    residuals = y_pred - y
    loss = (1 / (2 * len(y))) * np.sum(residuals ** 2)
    return loss
