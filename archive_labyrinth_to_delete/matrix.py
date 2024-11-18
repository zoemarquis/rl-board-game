from tile import Tile

DIMENSION = 7


class Matrix(object):
    """Class representing a matrix of NB_ROWS * NB_ROWS with default value in each cell"""

    def __init__(self, default_value=0):
        matrix = {}
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                matrix[(i, j)] = default_value
        self.matrix = matrix

    def get_value(self, row, col) -> Tile:
        """Return the value in the matrix at the line and column passed as parameters"""
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        return self.matrix[row, col]

    def set_value(self, row, col, value) -> None:
        """Set the value in the matrix at the line and column passed as parameters"""
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        self.matrix[row, col] = value

    def shift_row_left(self, row_index, updated_value=0) -> int:
        """Shifts the row at the index passed as parameter to the left by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert row_index >= 0 and row_index < DIMENSION, "Row index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert row_index % 1 == 0, "Row index must be odd"

        ejected_value = self.get_value(row_index, 0)
        for j in range(DIMENSION - 1):
            self.set_value(row_index, j, self.get_value(row_index, j + 1))
        self.set_value(row_index, DIMENSION - 1, updated_value)
        return ejected_value

    def shift_row_right(self, row_index, updated_value=0) -> int:
        """Shifts the row at the index passed as parameter to the right by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert row_index >= 0 and row_index < DIMENSION, "Row index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert row_index % 1 == 0, "Row index must be odd"

        ejected_value = self.get_value(row_index, DIMENSION - 1)
        for j in range(DIMENSION - 1, 0, -1):
            self.set_value(row_index, j, self.get_value(row_index, j - 1))
        self.set_value(row_index, 0, updated_value)
        return ejected_value

    def shift_column_up(self, col_index, updated_value=0) -> int:
        """Shifts the column at the index passed as parameter up by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert col_index >= 0 and col_index < DIMENSION, "Column index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert col_index % 1 == 0, "Column index must be odd"

        ejected_value = self.get_value(0, col_index)
        for i in range(DIMENSION - 1):
            self.set_value(i, col_index, self.get_value(i + 1, col_index))
        self.set_value(DIMENSION - 1, col_index, updated_value)
        return ejected_value

    def shift_column_down(self, col_index, updated_value=0):
        """Shifts the column at the index passed as parameter down by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert col_index >= 0 and col_index < DIMENSION, "Column index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert col_index % 1 == 0, "Column index must be odd"

        ejected_value = self.get_value(DIMENSION - 1, col_index)
        for i in range(DIMENSION - 1, 0, -1):
            self.set_value(i, col_index, self.get_value(i - 1, col_index))
        self.set_value(0, col_index, updated_value)
        return ejected_value
