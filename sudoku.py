import timeit
import_module = """
# Necessary imports
from charles.charles_file import Original, Population
from charles.selection import fps, tournament, ranking
from charles.crossover import cycle_co, pmx_co
from charles.mutation import swap_mutation, inversion_mutation
from puzzles import puzzle
import numpy as np
from matplotlib import pyplot as plt
"""
testcode = """
# Converting the original puzzle (which was a list) to a numpy array
original_puzzle_as_array = np.asarray([puzzle[x:x+9] for x in range(0, len(puzzle), 9)])
# Creating the original puzzle with the class Original
original_puzzle = Original(original_puzzle_as_array)

# We will run until finding a solution for the puzzle
solution_found = 0
# Each time we start a new population from the 0, we save the fitness of the best individual of every generation
fitness_values = []

while solution_found == 0:
    pop = Population(
        500,
        original_puzzle,
        "max"
    )

    solution_found, fitness = pop.evolve(
        gens=1000,
        select=ranking,
        crossover=pmx_co,
        mutate=swap_mutation,
        co_p=0.90,
        mu_p=0.15,
        elitism=5
    )

    fitness_values.append(fitness)

fitness_all = []
for sublist in fitness_values:
    for fitness_value in sublist:
        fitness_all.append(fitness_value)

generations = [generation for generation in range(len(fitness_all))]

#plt.plot(generations, fitness_all)
#plt.show()
print("Solution found in gen number: " + str(generations[-1]+1))
"""

times = timeit.repeat(stmt=testcode, setup=import_module, number=1, repeat=10)
print("Average time:" + str(round(sum(times)/len(times), 2)))
