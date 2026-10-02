"""

Implementation of the gradient descent algorithm.

"""
import numpy as np
from functions.decay_function import decay_function as function


def gradient_descent(x, y, learning_rate=0.0005, epochs=10000):
    """
    Gradient descent algorithm.
    :param x: ndarray of floats
    :param y: ndarray of floats
    :param learning_rate: float
    :param epochs: integer
    :return: ndarray of floats
    """
    theta = [0.0001, 0.005]
    loss_history = []
    grads = np.zeros(2)

    m = np.zeros(2)
    v = np.zeros(2)
    beta1 = 0.9
    beta2 = 0.999
    t = 0

    for epoch in range(epochs):
        y_pred = function(x, theta[0], theta[1])

        residuals = y_pred - y
        loss = (1 / (2 * len(y))) * np.sum(residuals ** 2)
        loss_history.append(loss)

        for i in range(2):
            theta_copy = theta.copy()
            theta_copy[i] += 1e-14
            y_pred_epsilon = function(x, theta_copy[0], theta_copy[1])

            residuals_epsilon = y_pred_epsilon - y
            grads[i] = (1 / len(y)) * np.sum(residuals_epsilon)

        t += 1

        m = beta1 * m + (1 - beta1) * grads
        v = beta2 * v + (1 - beta2) * (grads ** 2)

        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)

        theta -= learning_rate * m_hat / (np.sqrt(v_hat) + 1e-14)
    return theta
