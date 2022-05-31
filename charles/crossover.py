from random import randint, sample
import numpy as np
from charles.charles_file import Individual


def cycle_co(p1, p2):
    """
    Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # We start by creating the 2 offsprings, that are Individuals
    offspring1 = Individual()
    offspring2 = Individual()

    # The values from the 1st offspring are the same as the values from the 1st parent (and the same applies to the 2nd
    # offspring)
    offspring1.values = np.copy(p1.values)
    offspring2.values = np.copy(p2.values)

    # Then, we get 2 crossover points. We are going to perform the crossover from the row with index = crossover_point1,
    # until the row with index = crossover_point2
    crossover_point1 = randint(0, 8)
    crossover_point2 = randint(1, 9)

    # We don't want to have the same crossover points, since that would mean that we would be performing crossover
    # between just 1 row of the puzzle
    while crossover_point1 == crossover_point2:
        crossover_point1 = randint(0, 8)
        crossover_point2 = randint(1, 9)

    # If the first value is bigger than the 2nd, we just flip it, making the 1st = the 2nd, and the 2nd = the 1st
    if crossover_point1 > crossover_point2:
        temp = crossover_point1
        crossover_point1 = crossover_point2
        crossover_point2 = temp

    # Then, we go perform the crossover operation between rows with index = crossover_point1, until rows with
    # index = crossover_point2
    for i in range(crossover_point1, crossover_point2):
        offspring1.values[i], offspring2.values[i] = crossover_rows(offspring1.values[i], offspring2.values[i])

    # After performing all the operations, we return the 2 offsprings
    return offspring1, offspring2


def crossover_rows(row1, row2):
    """
    This function receives 2 rows (the rows with index i from the 2 parents), and performs cycle crossover between them
    At the end of all the operations, the function returns the new rows with index i for both offspring 1 and 2.
    """

    # We start the operation by creating 2 numpy arrays of 9 0's. The offspring_row1 is going to be the row with
    # index i in the 1st offspring; the offspring_row2 is going to be the row with index i in the 2nd offspring
    offspring_row1 = np.zeros(9, dtype=int)
    offspring_row2 = np.zeros(9, dtype=int)

    # We then create a list from 1 to 9 (all the values that a Sudoku row needs to have). Later, we are going to remove
    # from this list the values that were already used, in order to don't have repeated numbers in the rows.
    remaining = list(range(1, 10))

    cycle = 0

    # We will continue to perform the operation until the 2 rows that we are creating are completed
    while (0 in offspring_row1) and (0 in offspring_row2):
        # If we have even cycles
        if cycle % 2 == 0:
            # We will use the find_unused function, in order to get the index were we are going to start the cycle
            index = find_unused(row1, remaining)
            # We are going to start the cycle with the number that is in the index position in the original row from the
            # 1st parent
            start = row1[index]
            # We need to remove from the remaining list the number that we are going to use
            remaining.remove(row1[index])
            # On the new row for the 1st offspring, the value in the index position will be the same as in the original
            # row from the 1st parent
            offspring_row1[index] = row1[index]
            # On the new row for the 2nd offspring, the value in the index position will be the same as in the original
            # row from the 2nd parent
            offspring_row2[index] = row2[index]
            # Then, the next number to be considered will be the number that is in the index position in
            # the original row from the 2nd parent
            next = row2[index]

            # And we will perform the following, while the number where we are going isn't the same as the number from
            # where we started
            while next != start:
                # Next, we are going to use the find_value function to get the index of the next value in the original
                # row from the 1st parent
                index = find_value(row1, next)
                # So, on the new row for the 1st offspring, the value in the index position will be the same as in the
                # original row from the 1st parent
                offspring_row1[index] = row1[index]
                # We need to remove from the remaining list the number that we are going to use
                remaining.remove(row1[index])
                # On the new row for the 2nd offspring, the value in the index position will be the same as in the
                # original row from the 2nd parent
                offspring_row2[index] = row2[index]
                # Then, the next number to be considered will be the number that is in the index position in
                # the original row from the 2nd parent
                next = row2[index]
            # When we finally see that we are going next to the number from where we started, we can consider that the
            # cycle ended, and we add 1 to the current count of cycles
            cycle += 1

        # Otherwise, if we have odd cycles, we are going to flip the values
        else:
            # We will use the find_unused function, in order to get the index were we are going to start the cycle
            index = find_unused(row1, remaining)
            # We are going to start the cycle with the number that is in the index position in the original row from the
            # 1st parent
            start = row1[index]
            # We need to remove from the remaining list the number that we are going to use
            remaining.remove(row1[index])
            # Then, we are going to flip the values
            # On the new row for the 1st offspring, the value in the index position will be the same as in the original
            # row from the 2nd parent
            offspring_row1[index] = row2[index]
            # On the new row for the 2nd offspring, the value in the index position will be the same as in the original
            # row from the 1st parent
            offspring_row2[index] = row1[index]
            # Then, the next number to be considered will be the number that is in the index position in
            # the original row from the 2nd parent
            next = row2[index]

            # And we will perform the following, while the number where we are going isn't the same as the number from
            # where we started
            while next != start:
                # Next, we are going to use the find_value function to get the index of the next value in the original
                # row from the 1st parent
                index = find_value(row1, next)
                # On the new row for the 1st offspring, the value in the index position will be the same as in the
                # original row from the 2nd parent
                offspring_row1[index] = row2[index]
                # We need to remove from the remaining list the number that we are going to use
                remaining.remove(row1[index])
                # On the new row for the 2nd offspring, the value in the index position will be the same as in the
                # original row from the 1st parent
                offspring_row2[index] = row1[index]
                # Then, the next number to be considered will be the number that is in the index position in
                # the original row from the 2nd parent
                next = row2[index]
            # When we finally see that we are going next to the number from where we started, we can consider that the
            # cycle ended, and we add 1 to the current count of cycles
            cycle += 1

    # At the end, we return the new rows with index i for both offspring 1 and 2
    return offspring_row1, offspring_row2


def find_unused(parent_row, remaining):
    """
    This function searches in the parent_row if the number in the position with index i was already used in the new
    row. When the function finds a number that wasn't used until now, it returns the index of that number in the
    parent row.
    """

    for i in range(0, len(parent_row)):
        if parent_row[i] in remaining:
            return i


def find_value(parent_row, value):
    """
    This function searches in the parent_row a number that is given. We do this, in order to know what is the index
    of the next number in the original row of the 1st parent.
    """
    for i in range(0, len(parent_row)):
        if parent_row[i] == value:
            return i


def pmx_co(p1, p2):
    """
    Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # We start by creating the 2 offsprings, that are Individuals
    offspring1 = Individual()
    offspring2 = Individual()

    # The values from the 1st offspring are the same as the values from the 1st parent (and the same applies to the 2nd
    # offspring)
    offspring1.values = np.copy(p1.values)
    offspring2.values = np.copy(p2.values)

    # Then, we get 2 crossover points. We are going to perform the crossover from the row with index = crossover_point1,
    # until the row with index = crossover_point2
    crossover_point1 = randint(0, 8)
    crossover_point2 = randint(1, 9)

    # We don't want to have the same crossover points, since that would mean that we would be performing crossover
    # between just 1 row of the puzzle
    while crossover_point1 == crossover_point2:
        crossover_point1 = randint(0, 8)
        crossover_point2 = randint(1, 9)

    # If the first value is bigger than the 2nd, we just flip it, making the 1st = the 2nd, and the 2nd = the 1st
    if crossover_point1 > crossover_point2:
        temp = crossover_point1
        crossover_point1 = crossover_point2
        crossover_point2 = temp

    # Then, we go perform the crossover operation between rows with index = crossover_point1, until rows with
    # index = crossover_point2
    for i in range(crossover_point1, crossover_point2):
        offspring1.values[i], offspring2.values[i] = pmx_crossover_rows(offspring1.values[i], offspring2.values[i])

    # After performing all the operations, we return the 2 offsprings
    return offspring1, offspring2


def pmx_crossover_rows(row1, row2):
    """
    This function receives 2 rows (the rows with index i from the 2 parents), and performs partially matched/mapped
    crossover between them. At the end of all the operations, the function returns the new rows with index i for both
    offspring 1 and 2.
    """

    # We will start by choosing randomly 2 points, to get the window
    co_points = sample(range(len(row1)), 2)
    # Then, we sort those points, from the lowest to the biggest, to get the window for the crossover
    co_points.sort()

    def PMX(x, y):
        """
        The function where the actual PMX takes place. Receives 2 rows, performs all the operations inside
        the PMX crossover, and returns 1 row.
        """

        # We start by creating a list with 9 (the len of each row) None values
        o = [None] * len(x)

        # The values inside the window will be copied from the first parent, to the same position
        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        # We will see if there are any values in the window that we didn't use until now, and we will save them
        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

        # For each one of the values that are in the window that we didn't use until now:
        for i in z:
            temp = i
            # We start by seeing the position in the row of the 2nd parent of the I'th value that is in the window and
            # that we didn't use until now. Then, we get the value that is in that same position in the row of the 1st
            # parent. After that, we will see the position in the row of the 2nd parent of that same value. That will
            # be the index that we are saving.
            index = np.where(y == x[np.where(y == temp)])
            # Then, we will check in the offspring if in that same index we already have a value. We perform this check
            # until we find a position that is empty.
            while o[int(index[0])] is not None:
                # The temporary value is going to be the index that we have saved
                temp = int(index[0])
                # We will find where in the row of the 2nd parent is stored the value that we have in the position
                # that we have saved in the row of the 1st parent
                index = np.where(y == x[temp])
            # When we finally find a position in the offspring that is empty, we assign to that position the I'th value
            # that is in the window and that we didn't use until now.
            o[int(index[0])] = i

        # After using all the values in the window, but if we still don't have a full offspring, we are going to copy
        # to each empty position in the offspring the value that is in that position in the 2nd parent
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = PMX(row1, row2), PMX(row2, row1)
    return o1, o2
