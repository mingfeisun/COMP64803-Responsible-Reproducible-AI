"""

This code defines the Bayesian optimization algorithm.

"""

import skopt
from skopt.space import Real
import functions.loss_function


def bayes_optimiser(t, y):
    """
    Function which calculates the optimal parameters with Bayesian optimization.
    :param t: ndarray of floats
    :param y: ndarray of floats
    :return: ndarray of floats
    """
    space = [Real(0, 0.001, name="theta_0"), Real(0, 0.01, name="theta_1")]
    result = skopt.gp_minimize(lambda theta: functions.loss_function.objective_fixed(theta, t, y),
                               space, n_calls=100, random_state=0)
    optimal_theta = result.x
    return optimal_theta
