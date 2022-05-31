from random import randint, sample
from puzzles import puzzle
import numpy as np

puzzle_as_array = np.asarray([puzzle[x:x+9] for x in range(0, len(puzzle), 9)])


def swap_mutation(individual):
    """
    Implementation of swap mutation.

    Args:
        individual (Individual): Individual for mutation.

    Returns:
        Individual: One individual, resulting from the mutation.
    """

    # We start by getting 2 indexes. We are going to perform the mutation within those N rows, from the row with
    # index = mutation_rows1, until the row with index = mutation_rows2
    mutation_rows1 = randint(0, 8)
    mutation_rows2 = randint(1, 9)

    # If the first value is bigger than the 2nd, we just flip it, making the 1st = the 2nd, and the 2nd = the 1st
    if mutation_rows1 > mutation_rows2:
        temp = mutation_rows1
        mutation_rows1 = mutation_rows2
        mutation_rows2 = temp

    # Then, we go perform the mutation operation within rows with index = mutation_rows1, until rows with
    # index = mutation_rows2
    for i in range(mutation_rows1, mutation_rows2):
        individual.values[i] = SWAP(individual.values[i], i)

    # After performing all the operations, we return the offspring
    return individual


def SWAP(row, row_number):
    """
    This function receives one row and the row number, and performs swap mutation inside that row. At the end of the
    swap, the function returns the row with the elements swapped.
    """

    # We start by getting all the positions that are available for swapping (we don't want to perform mutation in the
    # elements that were given at the beginning of the puzzle)
    legal_values = [_ for _ in range(9)]
    # Then, for each of those values, we are going to see if they are really available or not
    for element in range(len(legal_values)):
        # If in the original puzzle, in that row_number and in that element we don't have a 0, that position is not
        # legal, so it will be removed from the legal_values list
        if puzzle_as_array[row_number][element] != 0:
            legal_values.remove(element)

    # After knowing which are the legal values to choose mutation points from, we choose without replacement 2 of them,
    # to perform the mutation
    mut_points = sample(legal_values, 2)
    # In the chosen row, in the position of the 1st mutation point, we are going to store the value that was originally
    # in the position of the 2nd mutation point (and vice-versa).
    row[mut_points[0]], row[mut_points[1]] = row[mut_points[1]], row[mut_points[0]]

    return row


def inversion_mutation(individual):
    """
    Implementation of inversion mutation.

    Args:
        individual (Individual): Individual for mutation.

    Returns:
        Individual: One individual, resulting from the mutation.
    """

    # We start by getting 2 indexes. We are going to perform the mutation within those N rows, from the row with
    # index = mutation_rows1, until the row with index = mutation_rows2
    mutation_rows1 = randint(0, 8)
    mutation_rows2 = randint(1, 9)

    # If the first value is bigger than the 2nd, we just flip it, making the 1st = the 2nd, and the 2nd = the 1st
    if mutation_rows1 > mutation_rows2:
        temp = mutation_rows1
        mutation_rows1 = mutation_rows2
        mutation_rows2 = temp

    # Then, we go perform the mutation operation within rows with index = mutation_rows1, until rows with
    # index = mutation_rows2
    for i in range(mutation_rows1, mutation_rows2):
        individual.values[i] = inversion(individual.values[i], i)

    # After performing all the operations, we return the offspring
    return individual


def inversion(row, row_number):
    """
    This function receives one row and the row number, and performs inversion mutation inside that row. At the end of
    the mutation, the function returns the row with the elements inverted.
    """

    mut_points = sample(range(len(row)), 2)
    mut_points.sort()
    until = int(len(range(mut_points[0], mut_points[1]+1))/2)

    count = 0
    for element in range(mut_points[0], mut_points[0]+until+1):
        if puzzle_as_array[row_number][element] == 0 and puzzle_as_array[row_number][mut_points[1]-count] == 0:
            row[element], row[mut_points[1]-count] = row[mut_points[1]-count], row[element]
        count += 1

    return row
