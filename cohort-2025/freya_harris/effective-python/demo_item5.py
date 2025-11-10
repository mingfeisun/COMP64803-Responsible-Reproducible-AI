# # before
# import numpy as np
# x = np.linspace(-10, 10, 1000)
# y = (1 / (1.5 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 0) / 1.5) ** 2)

# after
import numpy as np
def gaussian(x, mu=0, sigma=1.5):
    """ compute the gaussian distribution values for x"""
    return normalisation_factor(sigma) * np.exp(exponent_term(x, mu, sigma))

def normalisation_factor(sigma):
    """ return the normalisation constant 1 / (sigma * sqrt(2 * pi)) """
    return 1 / (sigma * np.sqrt(2 * np.pi))

def exponent_term(x, mu, sigma):
    """ return the exponent term -0.5 * ((x - mu) / sigma) ** 2 """
    return -0.5 * ((x - mu) / sigma) ** 2

x = np.linspace(-10, 10, 1000)
y = gaussian(x, mu=0, sigma=1.5)
