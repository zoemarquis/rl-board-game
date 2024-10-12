DIMENSION = 7


class Matrix(object):
    """Class representing a matrix of NB_ROWS * NB_ROWS with default value in each cell"""

    def __init__(self, default_value=0):
        matrix = {}
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                matrix[(i, j)] = default_value
        self.matrix = matrix

    def get_value(self, row, col):
        """Return the value in the matrix at the line and column passed as parameters"""
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        return self.matrix[row, col]

    def set_value(self, row, col, value):
        """Set the value in the matrix at the line and column passed as parameters"""
        self.matrix[row, col] = value

    def shift_row_left(self, row_index, updated_value=0):
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

    def shift_row_right(self, row_index, updated_value=0):
        """Shifts the row at the index passed as parameter to the right by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert row_index >= 0 and row_index < DIMENSION, "Row index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert row_index % 1 == 0, "Row index must be odd"

        ejected_value = self.get_value(row_index, DIMENSION - 1)
        for j in range(DIMENSION, 0, -1):
            self.set_value(row_index, j, self.get_value(row_index, j - 1))
        self.set_value(row_index, 0, updated_value)
        return ejected_value

    def shift_column_up(self, col_index, updated_value=0):
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
        for i in range(DIMENSION, 0, -1):
            self.set_value(i, col_index, self.get_value(i - 1, col_index))
        self.set_value(0, col_index, updated_value)
        return ejected_value

    # -----------------------------------------
    # INPUT / OUTPUT
    # -----------------------------------------

    # TODO tester utilité de la fonction
    def save_matrix(self, file_name):
        """Save the matrix in a text file"""
        file = open(file_name, "w")
        line = str(DIMENSION) + "," + str(DIMENSION) + "\n"
        file.write(line)
        for i in range(DIMENSION):
            line = ""
            for j in range(DIMENSION - 1):
                val = self.get_value(i, j)
                if val == None:
                    line += ","
                else:
                    line += str(val) + ","
            val = self.get_value(i, j + 1)
            if val == None:
                line += "\n"
            else:
                line += str(val) + "\n"
            file.write(line)
        file.close()

    # TODO tester utilité de la fonction
    def load_matrix(self, file_name, value_type="int"):
        """Load the matrix from a text file"""
        file = open(file_name, "r")
        line = file.readline()
        line = line.split(",")
        nb_rows = int(line[0])
        nb_cols = int(line[1])
        # Check if the matrix in the file has the same dimension as the matrix, nothing else is allowed
        assert (
            nb_rows == DIMENSION
        ), "Dimension of the matrix in the file is different from the dimension of the matrix"
        assert (
            nb_cols == DIMENSION
        ), "Dimension of the matrix in the file is different from the dimension of the matrix"
        matrix = Matrix()
        i = 0
        for row in file:
            values = row.split(",")
            j = 0
            for item in values:
                if item == "" or item == "\n":
                    self.set_value(i, j, None)
                elif value_type == "int":
                    self.set_value(i, j, int(item))
                elif value_type == "float":
                    self.set_value(i, j, float(item))
                elif value_type == "bool":
                    self.set_value(i, j, bool(item))
                else:
                    self.set_value(i, j, item)
                j += 1
            i += 1
        return matrix

    # TODO tester utilité de la fonction : seulement à affichage ?
    def print_divider_line(self, cell_size=4):
        print()
        for i in range(DIMENSION + 1):
            print("-" * cell_size + "+", end="")
        print()

    # TODO tester utilité de la fonction
    def print_matrix(self, cell_size=4):
        print(" " * cell_size + "|", end="")
        for i in range(DIMENSION):  # cols
            print(str(i).center(cell_size) + "|", end="")
        self.print_divider_line(cell_size)
        for i in range(DIMENSION):  # rows
            print(str(i).rjust(cell_size) + "|", end="")
            for j in range(DIMENSION):  # cols
                print(str(self.get_value(i, j)).rjust(cell_size) + "|", end="")
            self.print_divider_line(cell_size)
        print()
