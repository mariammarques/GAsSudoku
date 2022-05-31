"""
Here, we insert the different Sudoku Puzzles, as lists of 81 elements.
    The cells of the Sudoku puzzle that are not know in the beginning of the puzzle, are inserted in the list as 0's.
"""

# The puzzles that we present, are from a Sudoku app for Android smartphones, and the difficulty level is the one that
# was presented in the app

easy = [4, 0, 0, 0, 6, 5, 3, 8, 7,
        3, 8, 0, 7, 9, 4, 0, 2, 6,
        0, 6, 0, 3, 8, 0, 9, 4, 0,
        8, 0, 1, 0, 0, 0, 6, 0, 3,
        5, 0, 6, 0, 0, 8, 2, 1, 0,
        2, 7, 4, 1, 0, 6, 0, 0, 9,
        9, 5, 8, 0, 1, 3, 0, 0, 2,
        6, 4, 0, 0, 2, 9, 5, 3, 1,
        0, 0, 0, 6, 0, 0, 4, 0, 8]

medium = [0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 7, 0, 9, 6, 0, 8, 3, 5,
          0, 4, 9, 8, 0, 0, 7, 0, 0,
          0, 3, 0, 0, 0, 6, 1, 0, 0,
          8, 2, 0, 0, 1, 7, 0, 0, 9,
          0, 9, 1, 2, 5, 8, 6, 0, 0,
          0, 0, 0, 0, 0, 1, 4, 8, 0,
          2, 1, 4, 6, 0, 9, 3, 0, 0,
          7, 8, 0, 0, 0, 0, 0, 1, 0]

hard = [0, 0, 0, 4, 0, 0, 0, 0, 0,
        0, 9, 6, 0, 0, 0, 0, 2, 7,
        8, 3, 1, 0, 0, 0, 4, 0, 6,
        1, 0, 0, 3, 8, 0, 0, 0, 5,
        0, 0, 8, 6, 0, 9, 2, 0, 0,
        0, 0, 5, 0, 2, 0, 0, 0, 8,
        2, 8, 4, 5, 7, 6, 0, 9, 0,
        0, 0, 9, 0, 0, 8, 5, 0, 4,
        7, 5, 3, 9, 0, 0, 6, 8, 0]

very_hard = [0, 0, 0, 0, 6, 0, 0, 0, 0,
             4, 0, 9, 0, 0, 0, 7, 0, 2,
             2, 0, 0, 0, 5, 0, 0, 0, 6,
             0, 4, 0, 0, 1, 5, 0, 0, 0,
             0, 0, 8, 0, 0, 9, 5, 0, 7,
             0, 7, 0, 0, 2, 0, 0, 0, 0,
             7, 0, 0, 0, 9, 2, 1, 6, 0,
             8, 0, 5, 0, 0, 6, 9, 0, 0,
             0, 0, 0, 5, 0, 0, 8, 0, 0]

# Select the puzzle that you want to use in the sudoku solver
puzzle = very_hard
