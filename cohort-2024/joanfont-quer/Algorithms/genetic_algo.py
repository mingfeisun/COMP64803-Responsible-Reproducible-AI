"""

This code defines the genetic algorithm.

"""
import random
from functions.loss_function import objective_fixed


def create_population(size, bounds):
    """
    Creates a population of a specific size.
    :param size: Number of individuals created
    :param bounds: Maximum and minimum vaues each individual can have
    :return: ndarray of ndarrays of floats
    """
    population = []
    for _ in range(size):
        while True:
            theta = [random.uniform(*bound) for bound in bounds]
            if abs(theta[0] - theta[1]) > 0.0000001:
                population.append(theta)
                break
    return population


def mutates(theta, bounds, mutation_rate=0.1):
    """
    Randomly mutates an individual given some mutation rate.
    :param theta: ndarray of floats
    :param bounds: array of floats
    :param mutation_rate: float
    :return: ndarray of floats
    """
    new_theta = []
    for gene, (lower, upper) in zip(theta, bounds):
        if random.random() < mutation_rate:
            mutation = random.uniform(-0.1, 0.1)
            new_gene = gene + mutation
            new_gene = max(lower, min(upper, new_gene))
        else:
            new_gene = gene
        new_theta.append(new_gene)

    if abs(new_theta[0] - new_theta[1]) < 0.0000001:
        new_theta[1] += 0.0000001
    return new_theta


def crossover(parent1, parent2):
    """
    Calculates the average between two individuals, effectively produces an offspring.
    :param parent1: ndarray of floats
    :param parent2: ndarray of floats
    :return: ndarray of floats
    """
    return [(gene1 + gene2) / 2 for gene1, gene2 in zip(parent1, parent2)]


def genetic_algo(bounds, t, y, population_size=100, generations=100):
    """
    Implementation of the genetic algorithm.
    :param bounds: array of floats
    :param t: ndarray of floats
    :param y: ndarray of floats
    :param population_size: integer
    :param generations: integer
    :return: ndarray of floats
    """
    population = create_population(population_size, bounds)
    objective_with_data = lambda theta: objective_fixed(theta, t, y)

    for _ in range(generations):
        scores = [(theta, objective_with_data(theta)) for theta in population]
        scores.sort(key=lambda x: x[1])
        population = [x[0] for x in scores]

        selected = population[:population_size // 2]
        next_gen = []
        for i in range(population_size):
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            child = crossover(parent1, parent2)
            child = mutates(child, bounds)
            next_gen.append(child)
        population = next_gen

    best_individual = min(population, key=lambda theta: objective_with_data(theta))
    return best_individual
