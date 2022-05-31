from random import uniform, choice
from operator import attrgetter


def fps(population):
    """
    Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
    elif population.optim == "min":
        # Sum total fitness --> if we do 1/fitness, the individuals with smaller values of fitness
        # (which is better in minimization problems), will have a bigger chance of being selected
        total_fitness = sum([(1/i.fitness) for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += (1/individual.fitness)
            if position > spin:
                return individual


def tournament(population):
    """
    Tournament selection implementation. The size of the tournament will be 20% of the size of the population.
    This percentage can be selected when initializing the population.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: The best individual in the tournament.
    """

    # If the tournament size chosen is a valid percentage, the tournament size will be X% of the population size
    if 0 < population.tournament_size < 1:
        size = round((population.tournament_size * population.size))
    # If the tournament size chosen is not a valid percentage, the tournament size will be 20% of the population size
    else:
        size = round(0.20 * population.size)

    # Select individuals based on tournament size
    tournament_pop = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == "max":
        return max(tournament_pop, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament_pop, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")


def ranking(population):
    """
    Ranking selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # We start by sorting the population. With population.sort(), the population will already be sorted having in mind
    # if we are working with a minimization or a maximization problem
    population_sort = population.sort()

    # We will generate a random number between 0 and 0
    spin = uniform(0, 1)
    # Get a 'position' on the wheel
    position = 0
    # The variable "index" will be used to get the index of each individual.
    index = 1
    # The sum of indexes will be used for the probability of selecting an individual. The value will start as the len
    # of the population_sort list, which will be the size of our population
    sum_of_indexes = len(population_sort)

    # For each individual, we will add the respective index (starting in 1) to the sum_of_indexes
    for individual_index in range(len(population_sort)):
        sum_of_indexes += individual_index

    # Then, for each individual, we will say that the probability of being chosen is the position occupied by the
    # individual in the ranking, divided by the sum of the ranking indexes of all the individuals.
    for individual in population_sort:
        position += index/sum_of_indexes
        # If the spin lands in the position of that individual, we will return it
        if position > spin:
            return individual
        # At the end of each iteration, we need to add 1 to the variable index
        index += 1
    # For example, if we have a population with 3 individuals, the sum_of_indexes variable will start as 3. Then,
    # with the 1st for loop, we will run from 0 to 2. So, the sum_of_indexes will be 6, since 3+0=3; 3+1=4; 4+2=6.
    # 6 is, as we wanted, the sum of the ranking indexes of all the individuals (1+2+3=6). Then, with the 2nd for loop,
    # we will say that the position of the 1st individual is 1/6 (approximately 0.17); the position of the 2nd
    # individual will be 1/6 + 2/6 (0.5); and the position of the 3rd individual will be 1/6 + 2/6 + 3/6 (1). So, if
    # the spin, which is random, is for example 0.49, we will select the 2nd individual.
