"""
Level Class
"""
import numpy as np


class Level:
    """
    Creates a level object for the mega grid structure in the level editor
    """

    def __init__(self, matrix_rows, matrix_columns, mega_row, mega_column, starting_grid_row, starting_grid_column):
        self.number_of_matrix_rows = matrix_rows
        self.number_of_matrix_columns = matrix_columns
        self.mega_row = mega_row
        self.mega_column = mega_column
        self.curr_grid_row = starting_grid_row
        self.curr_grid_column = starting_grid_column
        self.scroll_direction = None
        self.grid = np.zeros((self.number_of_matrix_rows, self.number_of_matrix_columns), dtype=int)

    def resize_level_grid(self, matrix_rows, matrix_columns):
        """
        Resize the level's grid object
        :param matrix_rows: New row size
        :param matrix_columns: New column size
        """
        if (self.number_of_matrix_rows != self.number_of_matrix_rows or
                self.number_of_matrix_columns != matrix_columns):
            self.number_of_matrix_rows = matrix_rows
            self.number_of_matrix_columns = matrix_columns
            self.curr_grid_row = 0
            self.curr_grid_column = 0
            self.grid = np.zeros((self.number_of_matrix_rows, self.number_of_matrix_columns), dtype=int)
