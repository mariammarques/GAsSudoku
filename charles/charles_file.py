from random import random, randint
import numpy as np
from copy import deepcopy
from operator import attrgetter

import heapq


class Individual(object):
    """ An individual is a possible solution to the Sudoku puzzle """

    def __init__(self):
        self.values = np.zeros((9, 9), dtype=int)
        self.fitness = None
        return

    def get_fitness(self):
        """ A function to get the fitness for each possible solution to the Sudoku puzzle
            The fitness of an individual is calculated by (...)
            So, the higher the fitness, the better. The real solution to the puzzle will have a fitness of 1, and it
            will be a 9x9 grid of numbers, where in each row/column/grid we have the numbers 1 to 9, without duplicates

            Returns:
                float: the product between the column_sum and the grid_sum, as explained bellow, in the examples in the
                comments. The higher the fitness, the better the solution.
        """

        row_count = np.zeros(9)
        column_count = np.zeros(9)
        grid_count = np.zeros(9)
        row_sum = 0
        column_sum = 0
        grid_sum = 0

        # We will iterate through the 9 rows
        for i in range(0, 9):
            # And we will iterate through the 9 columns inside each row
            for j in range(0, 9):
                # Example:
                #    If we have a "7" on the 5th column of the 3rd row, we will go to the 6th (7-1) position of the
                #    row_count array, and we will sum 1 (because we found 1 more time the number 7) to the number that
                #    we already had in that position. So, in that way, we know how many times we found that number
                row_count[self.values[i][j] - 1] += 1
            # Ideally, the set(row_count) would be {1.0}, which would mean that we found each number 1 time in the row
            # The higher the row_sum, the better. In the perfect scenario, in which we had each number just 1 time in
            # each row, after iterating for each one of the 9 rows, we would sum 0.1111111111111111. After the 9 rows,
            # the row_sum would be 1.
            row_sum += (1.0 / len(set(row_count))) / 9
            # After each row, we restart the row_count
            row_count = np.zeros(9)

        # We will iterate through the 9 columns
        for i in range(0, 9):
            # And we will iterate through the 9 rows inside each column
            for j in range(0, 9):
                # The logic is the same as explained above, but this time is for the columns
                column_count[self.values[j][i] - 1] += 1
            # The logic is the same as explained above, but this time is for the columns
            column_sum += (1.0 / len(set(column_count))) / 9
            # After each column, we restart the column_count
            column_count = np.zeros(9)

        # We will iterate through the 9 blocks (each block has 3 rows --> we will go from row 0 to 8, with steps of 3)
        for i in range(0, 9, 3):
            # Each block has 3 columns --> we will go from column 0 to 8, with steps of 3
            for j in range(0, 9, 3):
                # Doing the same as above, for the first row/column of the grid
                grid_count[self.values[i][j] - 1] += 1
                # Doing the same as above, for the first row and second column of the grid
                grid_count[self.values[i][j + 1] - 1] += 1
                # Doing the same as above, for the first row and third column of the grid
                grid_count[self.values[i][j + 2] - 1] += 1
                # Doing the same as above, for the second row and first column of the grid
                grid_count[self.values[i + 1][j] - 1] += 1
                # Doing the same as above, for the second row and second column of the grid
                grid_count[self.values[i + 1][j + 1] - 1] += 1
                # Doing the same as above, for the second row and third column of the grid
                grid_count[self.values[i + 1][j + 2] - 1] += 1
                # Doing the same as above, for the third row and first column of the grid
                grid_count[self.values[i + 2][j] - 1] += 1
                # Doing the same as above, for the third row and second column of the grid
                grid_count[self.values[i + 2][j + 1] - 1] += 1
                # Doing the same as above, for the third row and third column of the grid
                grid_count[self.values[i + 2][j + 2] - 1] += 1

                # We will do the same as we did above
                grid_sum += (1.0 / len(set(grid_count))) / 9
                grid_count = np.zeros(9)

        # Next, we will calculate the fitness for the individual itself
        # If we got only unique elements in the rows, in the columns, and in the grids, the fitness will be 1, and we
        # have found a solution
        if int(row_sum) == 1 and int(column_sum) == 1 and int(grid_sum) == 1:
            fitness = 1.0
        # If we don't have only unique elements in the rows and/or in the columns and/or in the grids, the fitness will
        # be the product between the column_sum and the grid_sum (in the creation of the individuals, we forced the
        # solution, in order to not have duplicate values in the row)
        else:
            fitness = column_sum * grid_sum

        self.fitness = fitness
        return

    def __len__(self):
        return self.values.size

    def __getitem__(self, tup):
        x, y = tup
        return self.values[x][y]

    def __setitem__(self, tup, value):
        x, y = tup
        self.values[x][y] = value

    def __repr__(self):
        return f"Individual(size={self.values.size}); Fitness: {self.fitness}; Values: \n{self.values}"


class Original(Individual):
    """ The values that are known at the beginning of the Sudoku puzzle """

    def __init__(self, values):
        self.values = values
        return

    def duplicated_in_row(self, row, value):
        """ This checks if there are duplicated values in a certain row """
        # We will iterate, for the specific row, through the columns
        for column in range(0, 9):
            # If the value exists in any of the columns in that row, we will return "True", which means that there are
            # duplicated values in the row
            if self.values[row][column] == value:
                return True
        # Otherwise, if there are no duplicated values in the row, we return "False"
        return False

    def duplicated_in_column(self, column, value):
        """ This checks if there are duplicated values in a certain column """
        # We will iterate, for the specific column, through the rows
        for row in range(0, 9):
            # If the value exists in any of the rows in that column, we will return "True", which means that there are
            # duplicated values in the column
            if self.values[row][column] == value:
                return True
        # Otherwise, if there are no duplicated values in the column, we return "False"
        return False

    def duplicated_in_grid(self, row, column, value):
        """ This checks if there are duplicated values in a certain grid """
        # If row = 0 --> i = 0          # If row = 1 --> i = 0          # If row = 2 --> i = 0
        # If row = 3 --> i = 3          # If row = 4 --> i = 3          # If row = 5 --> i = 3
        # If row = 6 --> i = 6          # If row = 7 --> i = 6          # If row = 8 --> i = 6
        # This will allow us to get the first row (and the same happens for the columns) of the grids (which start in
        # the rows with index 0, 3 and 6)
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        # If the value exists in any of the positions of that grid, we will return "True", which means that there are
        # duplicated values in the grid
        if ((self.values[i][j] == value)
                or (self.values[i][j + 1] == value)
                or (self.values[i][j + 2] == value)
                or (self.values[i + 1][j] == value)
                or (self.values[i + 1][j + 1] == value)
                or (self.values[i + 1][j + 2] == value)
                or (self.values[i + 2][j] == value)
                or (self.values[i + 2][j + 1] == value)
                or (self.values[i + 1][j + 2] == value)):
            return True
        else:
            return False

    def __repr__(self):
        return f"Original Puzzle: {self.values}"


class Population(object):
    """ The population is a set of possible solutions (individuals) to the Sudoku puzzle """

    def __init__(self, size, original_sudoku, optim, tournament_size=0.2):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.tournament_size = tournament_size

        # We will get the legal values that each cell on the Sudoku puzzle can receive
        legal = Individual()
        legal.values = [[[] for _ in range(0, 9)] for _ in range(0, 9)]
        # We will iterate from the first (with index = 0) to the last (with index = 8) row
        for row in range(0, 9):
            # We will iterate from the first (with index = 0) to the last (with index = 8) column
            for column in range(0, 9):
                # We will iterate from the first (with value = 1) to the last (with value = 9) possible value
                for value in range(1, 10):
                    # We will check some conditions in the original data, to see if the value is available or given
                    # The conditions for being available are:
                    #   1. In the original data, in the same position, we have a 0 (AND);
                    #   2. (using the property --> "NOT(A or B)" is equal to "NOT A AND NOT B")
                    #     2.1. The value doesn't exist in that column, in the original data (AND)
                    #     2.2. The value doesn't exist in that grid (3x3), in the original data (AND)
                    #     2.3. The value doesn't exist in that row, in the original data
                    if ((original_sudoku.values[row][column] == 0) and
                            not (original_sudoku.duplicated_in_column(column, value)
                                 or original_sudoku.duplicated_in_grid(row, column, value)
                                 or original_sudoku.duplicated_in_row(row, value))):
                        # The value is available
                        legal.values[row][column].append(value)
                    elif original_sudoku.values[row][column] != 0:
                        legal.values[row][column].append((original_sudoku.values[row][column]))
        # Next, we are going to append individuals to the population
        for _ in range(size):
            # We will initialize 1 candidate (=individual) at a time
            candidate = Individual()
            # We will create the candidate row by row
            for i in range(0, 9):
                # The row is going to start as nine 0's
                row = np.zeros(9)
                # Then, we will fill the cells in that row
                for j in range(0, 9):
                    # If the value in that combination row/column was given, we will take it
                    if original_sudoku.values[i][j] != 0:
                        row[j] = original_sudoku.values[i][j]
                    # If the value in that position wasn't given, we will select one randomly from the legal values for
                    # that same position
                    elif original_sudoku.values[i][j] == 0:
                        row[j] = legal.values[i][j][randint(0, len(legal.values[i][j]) - 1)]
                # We can't have duplicate values in the row, so we will try again until we have a valid row
                while len(list(set(row))) != 9:
                    for j in range(0, 9):
                        if original_sudoku.values[i][j] == 0:
                            row[j] = legal.values[i][j][randint(0, len(legal.values[i][j]) - 1)]
                # Finally, we have the row with index i of the candidate (and we do this 9 times, for the 9 rows)
                candidate.values[i] = row
            # When we have all the cells of the candidate, we append it to the population
            self.individuals.append(candidate)

        # After having all the individuals in the population, we are going to calculate their fitness
        self.calculate_fitness()

        print("All individuals were created!")
        return

    def calculate_fitness(self):
        """ To update the fitness of every individual in the population """
        for individual in self.individuals:
            individual.get_fitness()
        return

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism=-1):
        # We will create a list where we will save the fitness of the best individual of each generation, in order
        # to help us to understand if we are stopped in a solution and not improving the fitness
        best_fitness = []
        # This value will increase every time that the fitness doesn't improve
        stopped_fitness = 0
        # This value will become 1 if we found a solution
        solution_found = 0
        # We will run for N generations
        for gen in range(gens):
            # In each generation, we are going to create a new population
            new_pop = []
            # If we say that elitism == 1, we are saying that we want the standard elitism
            if elitism == 1:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))
            # If we say that 0 < elitism < 1, we are going to perform elitism with percentages. So, for example, if
            # we say that elitism == 0.1, we are going to delete the worse 10% of the new population, and we are going
            # to insert the top 10% of individuals
            elif 0 < elitism < 1:
                if self.optim == "max":
                    elite = deepcopy(heapq.nlargest(round(elitism*self.size), self.individuals,
                                                    key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(heapq.nsmallest(round(elitism*self.size), self.individuals,
                                                     key=attrgetter("fitness")))
            # If we say that 1 < elitism < self.size, we are going to perform elitism with N individuals. So, for
            # example, if we say that elitism == 3, we are going to delete the worse 3 individuals of the new
            # population, and we are going to insert the top 3 of individuals
            elif 1 < elitism < self.size:
                if self.optim == "max":
                    elite = deepcopy(heapq.nlargest(round(elitism), self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(heapq.nsmallest(round(elitism), self.individuals, key=attrgetter("fitness")))
            # If we don't specify the elitism when calling the evolve function, or if we insert a number <= 0, or a
            # number that is bigger than the number of individuals in the population, elitism is not going to be
            # performed

            # We are going to see if we perform crossover and mutation operations, until we have a new population with
            # the same size as the original population
            while len(new_pop) < self.size:
                # With the specified selection algorithm, we are going to select 2 individuals as parents
                parent1, parent2 = select(self), select(self)
                # We are going to generate a random number between 0 and 1. If the number is smaller than the
                # crossover probability that we specified when calling the evolve function, we are going to perform
                # the selected crossover method
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                # Otherwise, we are not going to perform any type of crossover, and we are just going to say that the
                # 2 offsprings are the same as the 2 parents chosen
                else:
                    offspring1, offspring2 = parent1, parent2
                # We are going to generate a random number between 0 and 1. If the number is smaller than the
                # mutation probability that we specified when calling the evolve function, we are going to perform
                # the selected mutation method to the 1st offspring
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                # We are going to do the same a 2nd time, to see if we also apply mutation to the 2nd offspring
                if random() < mu_p:
                    offspring2 = mutate(offspring2)

                # After all of that, we are going to append the offspring1 to the new population
                new_pop.append(offspring1)
                # If we still have space in the new population, we are also going to insert the 2nd offspring in the
                # new population
                if len(new_pop) < self.size:
                    new_pop.append(offspring2)

            # After having all the individuals from the new population created, we are going to say that
            # the individuals from the population of that generation are the ones in the new_pop, and we are going
            # to calculate their fitness
            self.individuals = new_pop
            self.calculate_fitness()
            # After that, we are going to get the individuals that are going to be deleted from the new population, in
            # the case that we are working with any type of elitism

            # If we are performing the standard elitism, we need to get the individual with the worst fitness
            if elitism == 1:
                # If we have a maximization problem, the selected will be the individual with the lowest fitness
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                # If we have a minimization problem, the selected will be the individual with the highest fitness
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                # We need to remove from the new population the selected individual
                new_pop.pop(new_pop.index(least))
                # And then, we need to append to the new population the individual that was selected as the elite
                new_pop.append(elite)
            # If we are performing elitism with percentages, we need to get the X% individuals with the worst fitness
            elif 0 < elitism < 1:
                # If we have a maximization problem, the selected will be the individuals with the lowest fitness
                if self.optim == "max":
                    least = heapq.nsmallest(round(elitism*self.size), self.individuals, key=attrgetter("fitness"))
                # If we have a minimization problem, the selected will be the individuals with the highest fitness
                elif self.optim == "min":
                    least = heapq.nlargest(round(elitism*self.size), self.individuals, key=attrgetter("fitness"))
                # We need to remove from the new population the selected individuals
                for least_element in least:
                    new_pop.pop(new_pop.index(least_element))
                # And then, we need to append to the new population the individuals that were selected as the elite
                for elite_element in elite:
                    new_pop.append(elite_element)
            # If we are performing elitism with N > 1, we need to get the N individuals with the lowest fitness
            elif 1 < elitism < self.size:
                # If we have a maximization problem, the selected will be the individuals with the lowest fitness
                if self.optim == "max":
                    least = heapq.nsmallest(round(elitism), self.individuals, key=attrgetter("fitness"))
                # If we have a minimization problem, the selected will be the individuals with the highest fitness
                elif self.optim == "min":
                    least = heapq.nlargest(round(elitism), self.individuals, key=attrgetter("fitness"))
                # We need to remove from the new population the selected individuals
                for least_element in least:
                    new_pop.pop(new_pop.index(least_element))
                # And then, we need to append to the new population the individuals that were selected as the elite
                for elite_element in elite:
                    new_pop.append(elite_element)

            # Then, at the end of each generation, we are just going to print the best individual of the generation
            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                best_individual = max(self, key=attrgetter("fitness"))
            elif self.optim == "min":
                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                best_individual = min(self, key=attrgetter("fitness"))

            # If we found a solution, the program will stop
            if best_individual.fitness == 1:
                print("Solution found!")
                solution_found = 1
                best_fitness.append(best_individual.fitness)
                break

            # At the end of every generation, we are going to save the fitness of the best individual
            best_fitness.append(best_individual.fitness)

            # If we see that we didn't improve the fitness from the last generation, we are going to increment 1 to the
            # variable stopped_fitness
            if gen != 0 and best_fitness[gen] == best_fitness[gen-1]:
                stopped_fitness += 1

            # If we were stuck 100 times, we are going to restart the population
            if stopped_fitness >= int(0.1*gens):
                print("The solutions got stuck... Re-starting the population...")
                break

        return solution_found, best_fitness

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"

    def sort(self):
        if self.optim == "max":
            return sorted(self.individuals, key=lambda x: x.fitness)
        elif self.optim == "min":
            return sorted(self.individuals, key=lambda x: x.fitness, reverse=True)
