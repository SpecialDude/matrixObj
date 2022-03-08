from fractions import Fraction
import copy
from random import randint


class Matrix:
    """
    MATRIX
    ------
    A simple class for basic matrix mathematical operations.
    The contructor takes in lists of number and/or Matrix object.
    Creates a new matrix Object

    eg. create a new Matrix object
        >>> a = Matrix([4, 2, 7], [7, -2, 0], [9, 1, -4])
        >>> a
        |4   2   7|
        |7  -2   0|
        |9   1  -4|

    create matrix from other matrix (Stacked Matrix)
        >>> b = Matrix([5, 6, 2], a)
        >>> b
        |5   6   2|
        |4   2   7|
        |7  -2   0|
        |9   1  -4|

    If the matrix's elements is passed in as list of list, Set the keyword-only argument 'input_type' of the Matrix constructor to 1 eg.
        >>> matrixRows = [  [4, 2, 5],
                            [0, 1, 8],
                            [3, 6, 1]   ]
        >>> c = Matrix(matrixRows, input_type=1)
        >>> c
        |4   2   5|
        |0   1   8|
        |3   6   1|
    """
    __tuple_of_supported_types = (int, float, Fraction, complex)
    __tuple_string_of_supported_types = ("int", "float", "complex", "Fraction")
    __user_defined_repr_present = False
    __user_repr = None

    def __init__(self, *lists_of_rows, input_type=0):
        matrix = list(copy.deepcopy(lists_of_rows))
        if input_type == 1:
            matrix = list(matrix[0])
          
        self.__align = 0
        self.__validate_matrix(matrix)          
        self.__matrix = matrix
        del(matrix)

    def __validate_matrix(self, matrix, mt="Row"):
        skip = False
        skip_times = 0
        i = 0
        while (i < len(matrix)):
            if not isinstance(matrix[i], (list, tuple, Matrix)):
                raise TypeError (f"\"{matrix[i]}\" --> Matrix {mt} must be a list or a tuple")
            if isinstance(matrix[i], tuple):
                matrix[i] = list(matrix[i])
            if isinstance(matrix[i], Matrix):
                its_matrix = matrix[i].getmatrix()
                for j in range(len(its_matrix)):
                    matrix.insert((i+1+j), its_matrix[j])
                self.__compare_align(matrix[i]._getalign())
                skip_times = len(its_matrix) - 1
                del(matrix[i])

            if mt == "Row":
                if (len(matrix[i]) != len(matrix[0])):
                    raise ValueError (f"{matrix[i]} != {matrix[0]} in size --> Matrix {mt}s must be of the same size")
            else:
                size_func_dict = {"row":self.columnsize, "column":self.rowsize}
                if len(matrix[i]) != size_func_dict[mt]():
                    raise ValueError (f"{matrix[i]} != {mt} size --> Matrix {mt}s must be of the same size")
            
            if skip_times > 0:
                if not skip:
                    skip = True
                else:
                    skip_times -= 1
                    if skip_times == 0:
                        skip = False
                    i += 1    
                    continue        
            for j in range(len(matrix[0])):
                if not isinstance(matrix[i][j], Matrix.__tuple_of_supported_types):
                     raise TypeError (f"{matrix[i][j]} --> Matrix Element must be a number type {Matrix.__tuple_string_of_supported_types}")
                self.__update_alignment(matrix[i][j])
            i += 1
    
    def __validate_list(self, list_element, mt):
        if isinstance(list_element, Matrix):
            raise TypeError (f"{list_element} {type(list_element)} --> {mt} to be inserted must be a one-dimension List object")
        self.__validate_matrix([list_element], mt)

    def __validate_type(self, object, compare_type, operator):
        if not isinstance(object, compare_type):
            raise TypeError (f"'{operator}' not supported between instances of '{Matrix.__name__}' and '{type(object).__name__}'")

    def __isavalidindex(self, index, mt, raise_exception=False, same=True, fix_negative_index=True):
        if not isinstance(index, int):
            raise TypeError (f"{index} --> Index must be an int")
        
        size_func_dict = {"row":self.rowsize, "column":self.columnsize}
        if index < 1 and fix_negative_index:
            index = index + size_func_dict[mt]()
        if (index < 1) or (index > size_func_dict[mt]()):
            if not raise_exception:
                return False
            if not same:
                index -= 1    
            raise IndexError (f"'{index}' --> {mt.title()} index out of range ")    
        return True

    def __update_alignment(self, element):
        newA = len(str(element))
        if newA > self.__align:
            self.__align = newA

    def _getalign(self):
        """Returns the highest length of string repr of elements of the matrix"""
        return self.__align

    def __compare_align(self, newA):
        if newA > self.__align:
            self.__align = newA

    def __interchange(self, i, j, mt="row"):
        """Interchange rows or columns of the matrix"""

        inter_matrix = self.copy()

        if mt == 'row':
            row1 = list(*self[i - 1].getmatrix())
            row2 = list(*self[j - 1].getmatrix())

            inter_matrix.setrow(i, row2)
            inter_matrix.setrow(j, row1)

        else:
            column1 = list(*self[:, i - 1].getmatrix())
            column2 = list(*self[:, j - 1].getmatrix())

            inter_matrix.setcolumn(i, column2)
            inter_matrix.setcolumn(j, column1)
        
        return inter_matrix

    def __multiplybyscalar(self, i, scalar, mt="row"):
        self.__validate_type(scalar, compare_type=Matrix.__tuple_of_supported_types, operator="*")
        scalar_mul_matrix = self.copy()

        if mt == 'row':
            row = list(*self[i - 1].getmatrix())

            Matrix.multiplyListByScalar(row, scalar)
            scalar_mul_matrix.setrow(i, row)

        else:
            column = list(*self[:, i - 1].getmatrix())

            Matrix.multiplyListByScalar(column, scalar)
            scalar_mul_matrix.setcolumn(i, column)
        
        return scalar_mul_matrix

    def __multiplyandadd(self, i, j, scalar, mt="row"):
        self.__validate_type(scalar, compare_type=Matrix.__tuple_of_supported_types, operator="*")
        mulandadd_matrix = self.copy()
        
        if mt == 'row':
            rowJ = list(*self[j - 1].getmatrix())
            rowI = list(*self[i - 1].getmatrix())            

            Matrix.multiplyListByScalar(rowJ, scalar)
            resultRow  = Matrix.addListsElements(rowI, rowJ)
            mulandadd_matrix.setrow(i, resultRow)
        
        else:
            columnJ = list(*self[:, j - 1].getmatrix())
            columnI = list(*self[:, i - 1].getmatrix())            

            Matrix.multiplyListByScalar(columnJ, scalar)
            resultColumn  = Matrix.addListsElements(columnI, columnJ)
            mulandadd_matrix.setcolumn(i, resultColumn)
        
        return mulandadd_matrix                

    # Object Attribute Getters and Setters
    def getmatrix(self):
        """Returns a copy of the matrix elements as a tuple of list"""
        return tuple(copy.deepcopy(self.__matrix))

    def getrow(self, index):
        """Returns a tuple of elements of the ith (index) row of the matrix"""
        if not self.__isavalidindex(index, mt="row"):
            return None
        return tuple(copy.deepcopy(self.__matrix[index - 1]))

    def getcolumn(self, index):
        """Returns a tuple of elements of the ith (index) column of the matrix"""
        if not self.__isavalidindex(index, mt="column"):
            return None
        index -= 1    
        return tuple([row[index] for row in self.__matrix])

    def getelement(self, row_index, column_index):
        """Returns the element in the specified row and column of the matrix"""
        if not self.__isavalidindex(row_index, mt="row"):
            return None
        if not self.__isavalidindex(column_index, mt="column"):
            return None
        return self.__matrix[row_index - 1][column_index - 1]

    def getdiagonals(self):
        """Returns the diagonal elements of a square matrix"""
        if not self.issquare():
            raise
        return tuple([self.__matrix[i][i] for i in range(self.rowsize())])

    def rowsize(self):
        """Returns the number of rows in the matrix"""
        return len(self.__matrix)

    def columnsize(self):
        """Returns the number of columns in the matrix"""
        return len(self.__matrix[0])

    def dimension(self):
        """Returns the size of the matrix as str in the format
        'rowxcolumn' e.g 4x4
        """
        return f"{self.rowsize()}x{self.columnsize()}"

    def shape(self):
        """Returns a tuple of the dimension of the matrix: (row, column)"""
        return (self.rowsize(), self.columnsize())
    
    def size(self):
        """Returns the total number of elements in the matrix"""
        return self.rowsize() * self.columnsize()

    def setrow(self, row_index, row_elements):
        """Set the Elements in the ith row of the matrix, i (row_index) must be between range 1 to rowsize\n
            to expand the rows of the matrix, use expandrow()
        """
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        self.__validate_list(row_elements, mt="row")
        
        self.__matrix[row_index - 1] = row_elements

    def setcolumn(self, column_index, column_elements):
        """Set the Elements in the ith column of the matrix, i (column_index) must be between range 1 to columnsize\n
            to expand the column of the matrix, use expandcolumn()
        """
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        self.__validate_list(column_elements, mt="column")

        column_index -= 1
        for i in range(len(column_elements)):
            self.__matrix[i][column_index] = column_elements[i]

    def setelement(self, row_index, column_index, element):
        """Change the value of [i][j]th element of the matrix
        e.g. to change the first element in the matrix 'mat' to 4
            >>> mat = Matrix([1, 2], [5, 3])
            >>> mat
            |1  2|
            |5  3|
            >>> mat.setelement(1, 1, 4)
            >>> mat
            |4  2|
            |5  3|
        """
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        if not isinstance(element, Matrix.__tuple_of_supported_types):
            raise TypeError (f"{element} --> Matrix Element must be a number type {Matrix.__tuple_string_of_supported_types}")
        
        self.__matrix[row_index - 1][column_index - 1] = element
        self.__update_alignment(element)

    def insertrow(self, row_index, row_elements):
        """To insert a new row to a specified ith row (row_index) position.
        Row position must be between 1 and the initial rowsize,
        to add more rows after the last row, use expandrow()
        """
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        self.__validate_list(row_elements, mt="row")

        self.__matrix.insert(row_index - 1, row_elements)

    def insertcolumn(self, column_index, column_elements):
        """To insert a new column to a specified ith column position.
        column position must be between 1 and the initial columnsize,
        to add more columns after the last column, use expandcolumn()
        """
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        self.__validate_list(column_elements, mt="column")

        column_index -= 1
        for i in range(len(column_elements)):
            self.__matrix[i].insert(column_index, column_elements[i])
    
    def removerow(self, row_index):
        """Remove a row from the matrix"""
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        del(self.__matrix[row_index-1])

    def removecolumn(self, column_index):
        """Remove a column from the matrix"""
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        column_index -= 1
        for i in range(self.rowsize()):
            del(self.__matrix[i][column_index])

    def removecolumnbyslice(self, slice_var):
        """Remove slice of columns from the matrix"""
        for i in range(self.rowsize()):
            del(self.__matrix[i][slice_var])        

    def expandrow(self, *list_of_rows, append="post", input_type=0):
        """
        To append more row to the end (post) or before the first row (pre) of the matrix.
        For pre append, set argument append="pre"
                >>> mat.expandrow(row_elements, append="pre")
        """
        rows = list(copy.deepcopy(list_of_rows))
        if input_type == 1:
            rows = list(rows[0])

        self.__validate_matrix(rows, mt="row")
        if append == "pre":
            self.__matrix = rows + self.__matrix
        else:     
            self.__matrix = self.__matrix + rows

    def expandcolumn(self, *list_of_columns, append="post", input_type=0):
        """
        To append more columns to the end (post) or before the first column (pre) of the matrix.
        For pre append, set argument append="pre"
                >>> mat.expandcolumn(column_elements, append="pre")
        """
        columns = list(copy.deepcopy(list_of_columns))
        if input_type == 1:
            columns = list(columns[0])
        self.__validate_matrix(columns, mt="column")

        for i in range(len(columns)):
            for j in range(len(columns[i])):
                if append == "pre":
                    self.__matrix[j].insert(i, columns[i][j])
                else:    
                    self.__matrix[j].append(columns[i][j])

    def copy(self):
        """Make a full copy of the matrix instance"""
        return copy.deepcopy(self) 

    # Magic Methods (Overloading Operators)
    def __default_repr(self):
        k = [ "|" + "    ".join([str(element).rjust(self.__align) for element in row]) + "|" for row in self.__matrix]
        jstr = "\n".join(k)
        m_str = "\n" + jstr
        return m_str

    def __str__(self):
        if Matrix.__user_defined_repr_present:
            return Matrix.__user_repr(self.getmatrix())
        return self.__default_repr()

    def __repr__(self):
        return "Matrix(" + self.__str__() + ")"

    def __eq__(self, other):
        self.__validate_type(object=other, compare_type=Matrix, operator="==")
        if self.dimension() != other.dimension():
            return False
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[0])):
                if self.__matrix[i][j] != other.__matrix[i][j]:
                    return False
        return True

    def __add__(self, other):
        self.__validate_type(other, compare_type=Matrix, operator="+")
        if self.dimension() != other.dimension():
            raise ValueError (f"{self.dimension()} and {other.dimension()} --> Matrices must be of the same order")
        added_matrix = [[self.__matrix[i][j] + other.__matrix[i][j] for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(added_matrix, input_type=1)

    def __sub__(self, other):
        self.__validate_type(other, compare_type=Matrix, operator="-")
        if self.dimension() != other.dimension():
            raise ValueError (f"{self.dimension()} and {other.dimension()} --> Matrices must be of the same order")
        sub_matrix = [[self.__matrix[i][j] - other.__matrix[i][j] for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(sub_matrix, input_type=1)

    def __mul__(self, other):
        self.__validate_type(other, compare_type=(Matrix, int), operator="*")
        if isinstance(other, Matrix):
            if self.columnsize() != other.rowsize():
                raise ValueError (f"{self.dimension()} and {other.dimension()} --> Undefined Product")
            multiplied = []
            for i in range(self.rowsize()):
                row = []
                for j in range(other.columnsize()):
                    mul = 0
                    for k in range(other.rowsize()):
                        mul += self.__matrix[i][k] * other.__matrix[k][j]
                    row.append(mul)
                multiplied.append(row)
            return Matrix(multiplied, input_type=1)

        if isinstance(other, Matrix.__tuple_of_supported_types):
            scalar_multiplication = [[self.__matrix[i][j] * other for j in range(self.columnsize())] for i in range(self.rowsize())]
            return Matrix(scalar_multiplication, input_type=1)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            if other.issquare() and self.columnsize() == other.rowsize():
                return self * other.inverse(infraction=True)
        self.__validate_type(other, compare_type=Matrix.__tuple_of_supported_types, operator="/")
        divident = [[self.__matrix[i][j] / other for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(divident, input_type=1)

    def __rtruediv__(self, other):
        self.__validate_type(other, compare_type=Matrix.__tuple_of_supported_types, operator="/")
        if not self.issquare():
            raise ValueError("Undefined operation --> division by a non-square matrix")
        return other * (self ** -1)

    def rational_division(self, integer):
        """Makes a rational division and returns a matrix object with elements as a fraction type"""        
        if isinstance(integer, int):
            divident = [[Fraction(self.__matrix[i][j], integer) for j in range(self.columnsize())] for i in range(self.rowsize())]
            return Matrix(divident, input_type=1)
        else:
            return self / integer

    def __floordiv__(self, other):
        self.__validate_type(other, compare_type=Matrix.__tuple_of_supported_types, operator="//")
        divident = [[self.__matrix[i][j] // other for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(divident, input_type=1)

    def pow(self, index):
        """
        Takes the power of each element in the matrix to the supplied index
        """
        self.__validate_type(index, compare_type=Matrix.__tuple_of_supported_types, operator="**")
        exponent = [[self.__matrix[i][j] ** index for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(exponent, input_type=1)
    
    def __pow__(self, other):
        self.__validate_type(other, compare_type=(int,), operator="**")
        if not self.issquare:
            raise ValueError('matrix is not a square matrix')
        if other < 0:
            return self.inverse(infraction=True) ** (-1 * other)
        return self.__power(other)

    def __power(self, index):
        if index == 0:
            return self.identity()
        if index == 1:
            return self.copy()
        return self * self.__power(index - 1)

    def __getitem__(self, index):
        if isinstance(index, int):  # Gets a particular row
            self.__isavalidindex(index + 1, mt="row", raise_exception=True, same=False)
            return Matrix(self.__matrix[index])
        if isinstance(index, slice):  # Gets couple of rows
            self.__isavalidindex(self.__start(index.start) + 1, mt='row', raise_exception=True, same=False)
            return Matrix(self.__matrix[index], input_type=1)    
        if isinstance(index, tuple):
            if len(index) > 2:
                raise IndexError (f"{index} --> Too many indices, {len(index)} indices were given for 2d matrix")
            if isinstance(index[0], slice):
                self.__isavalidindex(self.__start(index[0].start) + 1, mt="row", raise_exception=True, same=False)
                if isinstance(index[1], int):       # Gets a particular column or its slice
                    self.__isavalidindex(index[1] + 1, mt='column', raise_exception=True, same=False)                    
                    return Matrix(self.getcolumn(index[1] + 1)[index[0]])
                elif isinstance(index[1], slice):   # Gets couple of rows and/or their slice
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)
                    mat = self.__matrix[index[0]]
                    for i in range(len(mat)):
                        mat[i] = mat[i][index[1]]
                    return Matrix(mat, input_type=1)
            elif isinstance(index[0], int):         # Gets an element
                self.__isavalidindex(index[0] + 1, mt='row', raise_exception=True, same=False)
                if isinstance(index[1], int):                    
                    self.__isavalidindex(index[1] + 1, mt="column", raise_exception=True, same=False)
                    return self.__matrix[index[0]][index[1]]
                elif isinstance(index[1], slice):        # Gets a particular row and/or its slice
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)    
                    return Matrix(self.__matrix[index[0]][index[1]])
        raise IndexError (f"{index} --> Index must be an int and/or slice [:]")

    def __cal_indexes(self, sliceVar, column=False):
        start = sliceVar.start
        stop = sliceVar.stop
        step = sliceVar.step

        size = {False:self.rowsize, True:self.columnsize}
              
        if step == None:    
            step = 1
        if start == None:
            if step < 0:
                start = -1
            else:    
                start = 0
        if stop == None:
            stop = size[column]()   

        if start < 0:
            start = start + size[column]()
        if stop < 0:
            stop = stop + size[column]()
        elif stop >= size[column]() and step < 0:
            stop = -1
        
        list_of_indices = [i for i in range(start, stop, step)]
        return list_of_indices

    def __constant_list(self, value, rowsize, columnsize=None):
        self.__update_alignment(value)
        if columnsize != None:
            return [[value for j in range(columnsize)] for i in range(rowsize)]
        return [value for i in range(rowsize)]

    def __start(self, start):
        if not start:
            start = 0
        return start       

    def __setitem__(self, index, value):
        value = copy.deepcopy(value)

        if isinstance(index, int):  # Sets a particular row
            self.__isavalidindex(index + 1, mt="row", raise_exception=True, same=False)
            if isinstance(value, Matrix.__tuple_of_supported_types):
                value = self.__constant_list(value, self.columnsize())
            elif isinstance(value, (list, tuple)):
                self.__validate_list(value, mt="row")
            elif isinstance(value, Matrix):
                if not (value.isrowmatrix() or value.iscolumnmatrix()):
                    raise ValueError(f"{value} --> Invalid value, cannot copy in a matrix row")
                if value.iscolumnmatrix():
                    value = value.transpose()
                value = value.getrow(1)
                self.__validate_list(value, mt="row")
            else:
                raise ValueError(f"{value} --> Invalid type, cannot copy in a matrix row")     
            self.__matrix[index] = value
            return
        if isinstance(index, slice):  # sets couple of rows
            self.__isavalidindex(self.__start(index.start) + 1, mt='row', raise_exception=True, same=False)
            indices = self.__cal_indexes(index)
            if isinstance(value, Matrix.__tuple_of_supported_types):
                value = self.__constant_list(value, len(indices), self.columnsize())
            elif isinstance(value, (list, tuple)):
                if len(indices) == len(value):
                    self.__validate_matrix(value, mt="row")
                else:
                    raise ValueError(f"{value} --> unbound value for the supplied indices")
            elif isinstance(value, Matrix):
                value = value.getmatrix()
                if len(indices) != len(value):
                    raise ValueError(f"{value} --> unbound value for the supplied indices")
                self.__validate_matrix(value, mt="row")
            else:
                raise TypeError(f"{value} --> Invalid type, cannot copy in matrix row(s)")
            self.__matrix[index] = value
            return  
        if isinstance(index, tuple):
            if len(index) > 2:
                raise IndexError (f"{index} --> Too many indices, {len(index)} indices were given for 2d matrix")
            if len(index) < 2:
                raise IndexError (f"{index} --> Not enough index, {len(index)} index were given for 2d matrix")
            if isinstance(index[0], slice):
                self.__isavalidindex(self.__start(index[0].start) + 1, mt="row", raise_exception=True, same=False)
                if isinstance(index[1], int):       # Sets a particular column or its slice
                    self.__isavalidindex(index[1] + 1, mt='column', raise_exception=True, same=False)
                    indices = self.__cal_indexes(index[0])                    
                    if isinstance(value, Matrix.__tuple_of_supported_types):
                        value = self.__constant_list(value, len(indices))
                    elif isinstance(value, (list, tuple)):
                        if len(indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                    elif isinstance(value, Matrix):
                        if not (value.isrowmatrix() or value.iscolumnmatrix()):
                            raise ValueError(f"{value} --> Invalid value, cannot copy in matrix column")
                        if value.isrowmatrix():
                            raise ValueError(f"{value} --> Invalid value, cannot copy in a row matrix into column")
                            # value = value.transpose()
                        value = value.getcolumn(1)
                        if len(indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                    else:
                        raise TypeError(f"{value} --> Invalid type, cannot copy in matrix column")
                    column = list(self.getcolumn(index[1] + 1))
                    column[index[0]] = value
                    self.setcolumn(index[1] + 1, column)
                    return
                elif isinstance(index[1], slice):   # Matrix Slices
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)
                    matrix_indices = self.__cal_indexes(index[0])
                    row_indices = self.__cal_indexes(index[1], column=True)
                    if isinstance(value, Matrix.__tuple_of_supported_types):
                        value = self.__constant_list(value, len(matrix_indices), len(row_indices))
                    elif isinstance(value, (list, tuple)):
                        if len(matrix_indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                        if len(row_indices) != len(value[0]):
                            raise ValueError(f"{value[0]} --> unbound value for the supplied indices")
                        self.__validate_matrix(value)
                    elif isinstance(value, Matrix):
                        value = value.getmatrix()
                        if len(matrix_indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                        if len(row_indices) != len(value[0]):
                            raise ValueError(f"{value[0]} --> unbound value for the supplied indices")
                        self.__validate_matrix(value)
                    else:
                        raise TypeError(f"{value} --> Invalid Type, cannot copy into matrix")
                    for i in range(len(matrix_indices)):
                        self.__matrix[matrix_indices[i]][index[1]] = value[i]
                    return
            elif isinstance(index[0], int):
                self.__isavalidindex(index[0] + 1, mt='row', raise_exception=True, same=False)
                if isinstance(index[1], int):           # Sets Element                 
                    self.__isavalidindex(index[1] + 1, mt="column", raise_exception=True, same=False)
                    if isinstance(value, Matrix) and value.issingletonmatrix():
                        value = value.getelement(0, 0)
                    if not isinstance(value, Matrix.__tuple_of_supported_types):
                        raise TypeError (f"{value} --> Matrix Element must be a number type {Matrix.__tuple_string_of_supported_types} or a Singleton Matrix")
                    self.__matrix[index[0]][index[1]] = value        # Sets Element
                    self.__update_alignment(value)
                    return
                elif isinstance(index[1], slice):       # Sets a particular row or its slice
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)
                    column_indices = self.__cal_indexes(index[1], column=True)
                    if isinstance(value, Matrix.__tuple_of_supported_types):
                        value = self.__constant_list(value, len(column_indices))
                    elif isinstance(value, (tuple, list)):
                        if len(column_indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                        self.__validate_matrix([value])
                    elif isinstance(value, Matrix):
                        if not (value.isrowmatrix() or value.iscolumnmatrix()):
                            raise ValueError(f"{value} --> Invalid value, cannot copy into matrix row")
                        if value.iscolumnmatrix():
                            raise ValueError(f"{value} --> Invalid value, cannot copy column matrix into row")
                            # value = value.transpose()
                        value = value.getrow(1)
                        if len(column_indices) != len(value):
                            raise ValueError(f"{value} --> unbound value for the supplied indices")
                        self.__validate_matrix([value])
                    else:
                        raise TypeError(f"{value} --> Invalid type, cannot copy into matrix row")
                    self.__matrix[index[0]][index[1]] = value
                    return
        raise IndexError (f"{index} --> Index must be an int and/or slice [:]")

    def __delitem__(self, index):
        if isinstance(index, int):
            self.__isavalidindex(index + 1, mt="row", raise_exception=True, same=False)
            del(self.__matrix[index])
            return
        elif isinstance(index, slice):
            self.__isavalidindex(self.__start(index.start) + 1, mt="row", raise_exception=True, same=False)
            del(self.__matrix[index])
            return
        elif isinstance(index, tuple):
            if len(index) > 2:
                raise IndexError (f"{index} --> Too many indices, {len(index)} indices were given for 2d matrix")
            if isinstance(index[0], slice):
                self.__isavalidindex(self.__start(index[0].start) + 1, mt="row", raise_exception=True, same=False)                
                if isinstance(index[1], int):
                    matrix_indices = self.__cal_indexes(index[0])
                    self.__isavalidindex(index[1] + 1, mt="column", raise_exception=True, same=False)
                    if len(matrix_indices) != self.rowsize():
                        raise IndexError("Can only delete a complete column")
                    self.removecolumn(index[1] + 1)
                    return
                elif isinstance(index[1], slice):
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)
                    row_indices = self.__cal_indexes(index[1], column=True)
                    if len(row_indices) != self.columnsize():
                        column_indices = self.__cal_indexes(index[0], column=False)
                        if len(column_indices) == self.rowsize():
                            self.removecolumnbyslice(index[1])
                            return
                        raise IndexError("Can only delete a complete row(s) or column(s)")
                    del(self.__matrix[index[0]])
                    return
            elif isinstance(index[0], int):
                if isinstance(index[1], int):
                    raise IndexError("Cannot delete a single entry of a matrix")
                if isinstance(index[1], slice):
                    self.__isavalidindex(self.__start(index[1].start) + 1, mt="column", raise_exception=True, same=False)
                    row_indices = self.__cal_indexes(index[1], column=True)
                    if len(row_indices) != self.columnsize():
                        raise IndexError("Can only delete a complete row")
                    del(self.__matrix[index[0]])
                    return
        raise IndexError (f"{index} --> Index must be an int and/or slice [:]")

    # Other Matrix Operation Methods
    def transpose(self):
        """Returns the transpose of the matrix"""
        transposed = [[self.__matrix[j][i] for j in range(self.rowsize())] for i in range(self.columnsize())]
        return Matrix(transposed, input_type=1)
    
    def determinant_by_minor_expansion(self):
        """Returns the determinant of the matrix (Square Matrix)"""
        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')

        if self.rowsize() == 1:
            return self.__matrix[0][0]

        if self.rowsize() == 2:
            return (    (self.__matrix[0][0] * self.__matrix[1][1] ) - (self.__matrix[1][0] * self.__matrix[0][1])   )
        
        determinant = 0
        for j in range(self.rowsize()):
            matrix_copy = copy.deepcopy(self.__matrix)
            for i in range(self.columnsize()):
                del(matrix_copy[i][j])
            del(matrix_copy[0])
            determinant += ( (-1) ** (2+j) ) * self.__matrix[0][j] * Matrix(matrix_copy, input_type=1).determinant()
        return(determinant)
    
    def determinant(self):
        """Returns the determinant of the matrix (Square Matrix)"""

        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')

        matrix = self.copy()

        swaps = 0
        j = 0
        while j < matrix.columnsize() - 1 and j < matrix.rowsize() - 1:
            column = matrix.getcolumn(j + 1)

            if Matrix._isconstantlist(column, 0):
                j += 1
                continue
            pe = matrix.getrow(j + 1)[j]

            if pe == 0:
                column = column[j + 1 :]

                try:
                    index = column.index(1) + 1
                    index += j
                except ValueError:
                    for k in range(len(column)):
                        if column[k] != 0:
                            index = k + j + 1
                            break
                    else:
                        j += 1
                        continue
                
                matrix = matrix.elementary_operation(j + 1, index + 1)
                pe = matrix.getrow(j + 1)[j]
                swaps += 1
            
            
            ipe = Matrix._inverseof(pe, infraction=True)  
            
            e_column = list(enumerate(matrix.getcolumn(j + 1)))[j + 1 :]

            for index, element in e_column:
                if element == 0:
                    continue
                ielement = (-element) * ipe
                matrix = matrix.elementary_operation(index + 1, j + 1, scalar=ielement)
            
            j += 1
        
        d = 1
        for e in matrix.getdiagonals():
            d *= e
        return d * ((-1) ** swaps)
        
    def minor(self):
        """Returns the minor of the matrix (Square Matrix)"""
        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')
        if self.rowsize() == 1:
            raise ValueError ('cannot compute minor of 1x1 matrix')
        minor_matrix = []
        for i in range(self.rowsize()):
            row = []
            for j in range(self.columnsize()):
                matrix_copy = copy.deepcopy(self.__matrix)
                for k in range(self.rowsize()):
                    del(matrix_copy[k][j])
                del(matrix_copy[i])
                if self.rowsize() == 2:
                    element_minor = matrix_copy[0][0]
                else:
                    element_minor = Matrix(matrix_copy, input_type=1).determinant()
                row.append(element_minor)
            minor_matrix.append(row)
        return Matrix(minor_matrix, input_type=1)

    def minor_at_ij(self, i, j):
        """Returns the minor at i,j of the matrix (i, j indexed from 1)"""
        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')
        if self.rowsize() == 1:
            raise ValueError ('cannot compute minor of 1x1 matrix')

        self.__isavalidindex(i, mt='row', raise_exception=True, same=True, fix_negative_index=False)
        self.__isavalidindex(j, mt='column', raise_exception=True, same=True, fix_negative_index=False)

        matrix_copy = copy.deepcopy(self.__matrix)
        for k in range(self.rowsize()):
            del(matrix_copy[k][j-1])

        del(matrix_copy[i-1])

        if self.rowsize() == 2:
            element_minor = matrix_copy[0][0]
        else:
            element_minor = Matrix(matrix_copy, input_type=1).determinant()

        return element_minor       

    def cofactor(self):
        """Returns the cofactor of the matrix (Square Matrix)"""
        minor_matrix = self.minor().getmatrix()
        cofactor_matrix = [[(-1)**(i+j+2) * minor_matrix[i][j] for j in range(len(minor_matrix[0]))] for i in range(len(minor_matrix))]
        return Matrix(cofactor_matrix, input_type=1)

    def cofactor_at_ij(self, i, j):
        """Returns the cofactor of the matrix (Square Matrix)"""
        element_minor = self.minor_at_ij(i, j)

        return (-1)**(i+j) * element_minor

    def adjoint(self):
        """Returns the adjoint of the matrix i.e tranpose of the cofactor matrix (Square Matrix)"""
        adjoint_matrix = self.cofactor().transpose()
        return adjoint_matrix

    def inverse(self, *, infraction=False):
        """Returns the inverse of the matrix  (i.e adjoint / determinant).
        To make rational division (i.e to return the matrix elements as a fraction), set the keyword argument 'infraction'=True

        Raises ZeroDivisionError if the determinant is 0 (i.e the matrix is not invertible)"""
        determinant = self.determinant()
        if determinant == 0:
            raise ZeroDivisionError ('Matrix not Invertible')
        if infraction:
            return self.adjoint().rational_division(determinant)
        inverse_matrix = self.adjoint()/determinant
        return inverse_matrix

    def additiveinverse(self):
        """Returns the additive inverse of the matrix"""
        return self * -1

    def reduce_to_ltriangle(self, infraction=True):
        """Reduce matrix to a lower triangular matrix by Gaussian Elimination"""
        if self.rowsize() > self.columnsize():
            raise ValueError("Cannot reduce matrix(m x n) with m > n")
        
        matrix = self.copy()

        j = matrix.rowsize() - 1
        while j > 0:
            column = matrix.getcolumn(j + 1)

            if Matrix._isconstantlist(column, 0):
                j -= 1
                continue
            pe = matrix.getrow(j + 1)[j]

            if pe == 0:
                column = column[:j]

                try:
                    index = column.index(1)
                except ValueError:
                    for k in range(len(column) -1, -1, -1):
                        if column[k] != 0:
                            index = k
                            break
                    else:
                        j -= 1
                        continue
                             
                matrix = matrix.elementary_operation(j + 1, index + 1)
                pe = matrix.getrow(j + 1)[j]
                
            
            ipe = Matrix._inverseof(pe, infraction)  
            
            e_column = list(enumerate(matrix.getcolumn(j + 1)))[:j]

            for index, element in e_column:
                if element == 0:
                    continue
                ielement = (-element) * ipe
                matrix = matrix.elementary_operation(index + 1, j + 1, scalar=ielement)
            
            j -= 1
        if not matrix.issquare():
            return AugMatrix(matrix, matrix.rowsize())
        return Matrix(matrix)

    def reduce_to_utriangle(self, infraction=True):
        """Reduce matrix to a upper triangular matrix by Gaussian Elimination"""
        if self.rowsize() > self.columnsize():
            raise ValueError("Cannot reduce matrix(m x n) with m > n")
        
        matrix = self.copy()
        
        j = 0
        while j < matrix.columnsize()-1 and j < matrix.rowsize()-1:
            column = matrix.getcolumn(j + 1)

            if Matrix._isconstantlist(column, 0):
                j += 1
                continue
            pe = matrix.getrow(j + 1)[j]

            if pe == 0:
                column = column[j + 1 :]

                try:
                    index = column.index(1) + 1
                    index += j
                except ValueError:
                    for k in range(len(column)):
                        if column[k] != 0:
                            index = k + j + 1
                            break
                    else:
                        j += 1
                        continue

                """ if 1 in column:
                    index = column.index(1) + 1
                    index += j
                else:
                    for k in range(len(column)):
                        if column[k] != 0:
                            index = k + j + 1
                            break
                    else:
                        j += 1
                        continue """
                
                matrix = matrix.elementary_operation(j + 1, index + 1)
                pe = matrix.getrow(j + 1)[j]
            
            
            ipe = Matrix._inverseof(pe, infraction)
            
            e_column = list(enumerate(matrix.getcolumn(j + 1)))[j + 1 :]

            for index, element in e_column:
                if element == 0:
                    continue
                ielement = (-element) * ipe
                matrix = matrix.elementary_operation(index + 1, j + 1, scalar=ielement)
            
            j += 1
        if not matrix.issquare():
            return AugMatrix(matrix, matrix.rowsize())
        return Matrix(matrix)

    def rref(self, infraction=False):
        """Row Reduce matrix to Echelon Form, returns the reduced matrix
        \nSet argument 'infraction = True' to return the reduced Matrix in fraction.
        """
        matrix = self.copy()

        j = 0
        while j < matrix.columnsize() and j < matrix.rowsize():
            column = matrix.getcolumn(j + 1)

            if Matrix._isconstantlist(column, 0):
                j += 1
                continue

            pe = matrix.getrow(j + 1)[j]
            if pe == 0:
                column = column[j + 1 :]

                try:
                    index = column.index(1) + 1
                    index += j
                except ValueError:
                    for k in range(len(column)):
                        if column[k] != 0:
                            index = k + j + 1
                            break
                    else:
                        j += 1
                        continue
                
                matrix = matrix.elementary_operation(j + 1, index + 1)
                pe = matrix.getrow(j + 1)[j]
            
            if pe != 1:
                ipe = Matrix._inverseof(pe, infraction)
                matrix = matrix.elementary_operation(j + 1, scalar=ipe)
            
            e_column = list(enumerate(matrix.getcolumn(j + 1)))
            del e_column[j]

            for index, element in e_column:
                if element == 0:
                    continue
                ielement = -element
                matrix = matrix.elementary_operation(index + 1, j + 1, scalar=ielement)
            
            j += 1
        
        return Matrix(matrix.getmatrix(), input_type=1)
    
    def nonzeros(self, row=True):
        """Returns the number of Non-zero rows in a matrix.
        Set row=False for column"""
        r = 0
        if row:
            for row in self:
                if not row.iszeromatrix():
                    r += 1
        else:
            for j in range(self.columnsize()):
                if not self[:, j].iszeromatrix():
                    r += 1
        return r

    def rank(self):
        """Returns the rank of the matrix (i.e number of non-zero rows of the matrix in reduced echeon form)"""
        return self.rref(infraction=True).nonzeros()

    def trace(self):
        """Returns the sum of the diagonal elements"""
        return sum(self.getdiagonals())

    def sum(self):
        """Returns the sum of all elements of the matrix"""
        return sum([sum(i) for i in self.getmatrix()])

    # Elementary Operation
    def elementary_operation(self, i, j=None, *, scalar=None, row=True):
        """Perform Elementary operation on matrix (returns the new matrix).
        eg.
            >>> matA = Matrix([1, 1, 1], [2, 2, 2], [3, 3, 3])
        \nTo perform Ri(\u03b1)
            >>> elementary_operation(i, scalar=\u03b1)
            >>> matA.elementary_operation(2, scalar=2)
            |1   1   1|
            |4   4   4|
            |3   3   3|     
        \nFor Ri,j Operation
            >>> elementary_operation(i, j)
            >>> matA.elementary_operation(1, 3)
            |3   3   3|
            |2   2   2|
            |1   1   1|
        \nAnd for Ri,j(\u03b1) Operation
            >>> elementary_operation(i, j, scalar=\u03b1)
            >>> matA.elementary_operation(1, 2, scalar=2)
            |5   5   5|
            |2   2   2|
            |3   3   3|
        \nTo perform column operation i.e. Ci(\u03b1) set the 'row' argument to False
            >>> elementary_operation(i, scalar=\u03b1, row=False)
        \nNote: 'row' and 'scalar' are keyword-only arguments
        """
        if j == None and scalar == None:
            raise TypeError('Reqiured 1 more argument (jth row(col) or Scalar)')

        mt = 'row' if row else 'column'
        if j != None and scalar != None:
            return self.__multiplyandadd(i, j, scalar, mt)

        elif scalar != None:
            return self.__multiplybyscalar(i, scalar, mt)

        else:
            return self.__interchange(i, j, mt)
    
    # Property Methods
    def issquare(self):
        """Returns True if the matrix is a square matrix i.e. rowsize equals columnsize"""
        return self.rowsize() == self.columnsize()

    def isrowmatrix(self):
        """Returns True if the matrix is a row matrix i.e. rowsize equals 1"""
        return self.rowsize() == 1

    def iscolumnmatrix(self):
        """Returns True if the matrix is a column matrix i.e. columnsize equals 1"""
        return self.columnsize() == 1

    def isnormal(self):
        """Returns True if the matrix is Normal i.e  commutativity of matrix and its transpose
        \n(A * A\u1D40 = A\u1D40 * A)"""
        t = self.transpose()
        return self * t == t * self
    
    def isorthogonal(self):
        """Returns True if the matrix is Orthognal i.e product of matrix and its transpose yields Identity matrix
        \n(A * A\u1D40 = I)"""
        if not self.issquare():
            return False
        return self * self.transpose() == self.identity()
    
    def issingletonmatrix(self):
        """Returns True if the matrix is a Singleton matrix i.e. columnsize = rowsize = 1"""
        return self.columnsize() == 1 and self.rowsize() == 1
    
    def __isconstantmatrix(self, unit):
        for i in range(self.rowsize()):
            for j in range(self.columnsize()):
                if self.__matrix[i][j] != unit:
                    return False
        return True

    def isnull(self):
        """Returns True if the matrix is a zero matrix i.e. all elements equals 0"""
        return self.__isconstantmatrix(0)

    def iszeromatrix(self):
        """Returns True if the matrix is a zero matrix i.e. all elements equals 0"""
        return self.__isconstantmatrix(0)

    def isonesmatrix(self):
        """Returns True if the matrix is a ones matrix i.e. all elements equals 1"""
        return self.__isconstantmatrix(1)

    def isscalarmatrix(self):
        """Returns True if the matrix is a scalar matrix i.e all diagonal entries/elements are the same"""
        if not self.isdiagonal():
            return False
        if self[0,0] == 0:
            return False
        return isconstantlist(self.getdiagonals())
    
    def isscalarmatrixof(self, scalar):
        """Returns True if the matrix is a scalar matrix having a scalar value of the argument 'scalar'
        \nscalar cannot be zero, returns False for such case."""
        if not self.isdiagonal():
            return False
        if self[0,0] == 0:
            return False
        return isconstantlist(self.getdiagonals(), scalar)        
    
    def isconstantmatrix(self):
        """Returns True if the matrix is a contant matrix i.e all entries/elements are the same"""
        compare_number = self.__matrix[0][0]
        return self.__isconstantmatrix(compare_number)
    
    def isconstantmatrixof(self, number):
        """Returns True if the matrix is a constant matrix having a constant value of the argument 'number'"""
        return self.__isconstantmatrix(number)

    def symmetric(self):
        """Returns True if the matrix is symmetric i.e matrix is equal to its transpose"""
        return self.transpose() == self

    def skew(self):
        """Returns True if the matrix is skew"""
        return (self.transpose() * -1) == self

    def isdiagonal(self):
        """Returns True if the matrix is diagonal i.e every off-diagonal element is zero"""
        if not self.issquare():
            return False
        for i in range(self.rowsize()):
            for j in range(self.columnsize()):
                if i == j:
                    continue
                if self.__matrix[i][j] != 0:
                    return False
        return True
        
    def istriangular(self):
        """Returns True if matrix is a triangular matrix (Upper or Lower)"""
        return self.uppertriangle() or self.lowertriangle()

    def uppertriangle(self):
        """Returns True if elements (of every i > j) are non-zero elements"""
        if not self.issquare():
            return False
        for i in range(self.rowsize()):
            for j in range(self.columnsize()):
                if i <= j:
                    continue
                if self.__matrix[i][j] != 0:
                    return False
        return True

    def lowertriangle(self):
        """Returns True if elements (of every i < j) are non-zero elements"""
        if not self.issquare():
            return False
        for i in range(self.rowsize()):
            for j in range(self.columnsize()):
                if i >= j:
                    continue
                if self.__matrix[i][j] != 0:
                    return False
        return True

    def invertible(self):
        """Returns True if the matrix has inverse, i.e determinant != 0"""
        if not self.issquare():
            return False
        return self.determinant() != 0

    def identity(self, size=None):
        """Returns the Multiplicative Identity of the matrix. 
        \nIf size (in int) is specified, Returns Identity matrix of that dimension
        """
        if not self.issquare() and size == None:
            raise ValueError("Non square matrix can't have multiplicative Identity")
        if not size:
            size = self.rowsize()
        return generate_identity_matrix(size)
    
    def additiveidentity(self):
        """Returns the Additive Identity of the matrix (i.e. a zero matrix of the same dimension)
        """
        return self._unitgenerator(0, self.shape())

    def ones_matrix(self, shape=None):
        """Returns Ones matrix of specified 'shape'. 
        \nIf shape (in int) is not specified, Returns Ones matrix of the same dimension as the matrix instance that invokes the method
        """
        if not shape:
            shape = self.shape()
        return Matrix._unitgenerator(1, shape)

    def zero_matrix(self, shape=None):
        """Returns Zero matrix of specified 'shape'. 
        \nIf shape (in int) is not specified, Returns Zero matrix of the same dimension as the matrix instance that invokes the method
        """
        if not shape:
            shape = self.shape()
        return Matrix._unitgenerator(0, shape)

    def constant_matrix(self, number, shape=None):
        """Returns Constant matrix of the specified 'shape'. 
        \nIf shape (in int) is not specified, Returns Constant matrix of the same dimension as the matrix instance that invokes the method
        """
        if shape == None:
            shape = self.shape()   
        return Matrix._unitgenerator(number, shape)

    def random_matrix(self, lower, upper, shape=None):
        """Returns a randomly generated matrix of specified 'shape'. 
        \nIf shape (in int) is not specified, Returns random matrix of the same dimension as the matrix instance that invokes the method
        """
        if not shape:
            shape = self.shape()
        return random_matrix(lower, upper, shape)

    def random_constant_matrix(self, lower, upper, shape=None):
        """Returns random Constant matrix of specified 'shape'. 
        \nIf shape (in int) is not specified, Returns random Constant matrix of the same dimension as the matrix instance that invokes the method
        """
        if not shape:
            shape = self.shape()
        return Matrix._unitgenerator(randint(lower, upper), shape)

    
    # Class Methods
    @classmethod
    def setrepr(cls, func):
        """Change the string representation of the matrix class
        \nDefine a function that takes exactly one parameter and returns a string,then call the setrepr() method with the defined function's object as argument.
        \nThis function will be called when invoking the __str__() method and the matrix's element as a tuple of list will be passed in as argument
        \n\te.g. To simply represent the matrix as a list of list
                >>> def newrepr(matrix):
                    ... return str(list(matrix))
                    
                >>> Matrix.setrepr(newrepr)
                >>> mat = Matrix([1, 4, 5], [9, 3, 8], [4, 5, 8])
                >>> mat
                [[1, 4, 5], [9, 3, 8], [4, 5, 8]]
        
        Perform string manipulation on the passed argument 'matrix' in the defined function and return the string of the desired representation
                
        """
        
        cls.__user_repr = func
        cls.__user_defined_repr_present = True

    @classmethod
    def resetrepr(cls):
        """Reset back the String Representation of the Matrix class to the default representation."""
        cls.__user_defined_repr_present = False
        cls.__user_repr = None


    # Static Methods
    @staticmethod
    def _unitgenerator(unit, shape):
        """For Generating Matrices with constant values e.g[[3, 3, 3], [3, 3, 3], [3, 3, 3]]
        """
        if not isinstance(shape, tuple):
            raise TypeError (f"{shape} --> Required a tuple of matrix dimension e.g (2,3) for a 2x3 matrix")
        
        rowsize, columnsize = shape
        
        if rowsize == 0 or columnsize == 0:
            raise ValueError("row or column size cannot be zero")

        unitMatrix = [[unit for j in range(columnsize)] for i in range(rowsize)]
        return Matrix(unitMatrix, input_type=1)
    
    @staticmethod
    def _inverseof(num, infraction=False):
        if infraction and isinstance(num, int):
            return Fraction(1, num)
        return 1/num
    
    @staticmethod
    def _isconstantlist(li, unit):
        for num in li:
            if num != unit:
                return False
        return True
    
    @staticmethod
    def multiplyListByScalar(listObject, scalar):
        """Multiply individual element in a list by a number (scalar)"""
        for i in range(len(listObject)):
            listObject[i] *= scalar

    @staticmethod
    def addListsElements(*listObjects):
        """Add lists togther element by element"""
        result = []

        for i in range(len(listObjects[0])):
            sum = 0
            for j in range(len(listObjects)):
                sum += listObjects[j][i]
            result.append(sum)
        return result




class AugMatrix(Matrix):
    """
    Augmented Matrix
    ----------------
    Append the columns of two matrix to form an augmented matrix.
    Perform the same elementary operations on both matrices augmented together.
    \nThe contructor takes two arguments (matrix A and matrix B) which can be matrix objects or a list of matrix rows of both matrices

    >>> matA = Matrix([3, 5, 9], [1, -2, 0], [2, 3, 1])
    >>> b = [4, -5, 7]
    >>> augmentAB = AugMatrix(matA, augcolumn=b)
    >>> augmentAB
    AMatrix(
    | 3     5     9 |  4 |
    | 1    -2     0 | -5 |
    | 2     3     1 |  7 |)
    >>> 

    Augmented Matrix from two matrices
    >>> matA = Matrix([5, 7, 0], [1, -1, 2], [3, 0, 1])
    >>> matB = Matrix([1, 0, 9], [4, 2, 1], [2, 1, 0])
    >>>
    >>> augAB = AugMatrix(matA, matB)
    >>> augAB
    AMatrix(
    | 5     7     0 |  1     0     9 |
    | 1    -1     2 |  4     2     1 |
    | 3     0     1 |  2     1     0 |)
    >>> 

    If a second matrix is not supplied, the first matrix is augmented with it's last column as the augmented part
    >>> c = Matrix([-2, 3, 1, 5], [3, 0, 9, 2], [1, 2, 9, 0])
    >>> augC = AugMatrix(c)
    >>> augC
    AMatrix(
    |-2     3     1 |  5 |
    | 3     0     9 |  2 |
    | 1     2     9 |  0 |)
    >>> 

    If a second integer argument is suppied, the first matrix is augmented by indexing from the integer argument
    >>> d = Matrix([4, 5, 0, 1, -1], [-2, 2, 1, 3, -1], [3, 7, 0, -5, 2])
    >>> augD = AugMatrix(d, 3)
    AMatrix(
    | 4     5     0 |  1    -1 |
    |-2     2     1 |  3    -1 |
    | 3     7     0 | -5     2 |)
    >>>
    """

    def __init__(self, matrix, augcolumn=None):
        self.__fullmatrix = Matrix(*matrix)

        if augcolumn:
            if isinstance(augcolumn, Matrix):
                if not augcolumn.isrowmatrix():
                    augcolumn = augcolumn.transpose()
                augcolumn = augcolumn.getmatrix()

            elif isinstance(augcolumn, (list, tuple)):
                if not isinstance(augcolumn[0], (list, tuple)):
                    augcolumn = [augcolumn]
            
            elif isinstance(augcolumn, int):
                self.augindex = augcolumn
                return        
            
            else:
                augcolumn = [augcolumn]

            self.__fullmatrix.expandcolumn(*augcolumn)
            self.augindex = self.__fullmatrix.columnsize() - len(augcolumn)
        else:
            self.augindex = self.__fullmatrix.columnsize() - 1

    @property
    def matrix(self):
        """Returns the first matrix of the augmented matrix."""
        return self.__fullmatrix[:, :self.augindex]
    
    @property
    def augcolumn(self):
        """Returns the augmented column of the augmented (the second matrix)."""
        return self.__fullmatrix[:, self.augindex:]
    
    @property
    def _Matrix__matrix(self):
        return list(self.__fullmatrix.getmatrix())
     
    def _Matrix__default_repr(self):
        k = ["|" + "    ".join([str(self.matrix[i, j]).rjust(self.__fullmatrix._Matrix__align) for j in range(self.matrix.columnsize())]) + " | " + "    ".join([str(self.augcolumn[i, k]).rjust(self.__fullmatrix._Matrix__align) for k in range(self.augcolumn.columnsize())]) + " |" for i in range(self.matrix.rowsize())]
        jstr = "\n".join(k)
        m_str = "\n" + jstr
        return m_str

    @property
    def _Matrix__align(self):
        return self.__fullmatrix._Matrix__align
    
    def __repr__(self):
        return "AMatrix(" + self.__str__() + ")"

    def rref(self, infraction=False):
        """Row Reduce the augmented matrix to Echelon Form, returns the reduced matrix
        \nSet argument 'infraction = True' to return the reduced Matrix in fraction.
        """
        amatrix = self.copy()

        j = 0

        while j < amatrix.matrix.columnsize() and j < amatrix.matrix.rowsize():
            column = amatrix.matrix.getcolumn(j + 1)

            if amatrix._isconstantlist(column, 0):
                j += 1
                continue

            pe = amatrix.matrix.getrow(j + 1)[j]

            if pe == 0:
                column = column[j + 1 :]

                try:
                    index = column(1) + 1
                    index += j
                except ValueError:
                    for k in range(len(column)):
                        if column[k] != 0:
                            index = k + j + 1
                            break
                    else:
                        j += 1
                        continue
                
                amatrix = AugMatrix(amatrix.__fullmatrix.elementary_operation(j + 1, index + 1), amatrix.augindex)
                pe = amatrix.matrix.getrow(j + 1)[j]

            if pe != 1:
                ipe = amatrix._inverseof(pe, infraction)
                amatrix = AugMatrix(amatrix.__fullmatrix.elementary_operation(j + 1, scalar=ipe), amatrix.augindex)
            
            e_column = list(enumerate(amatrix.matrix.getcolumn(j + 1)))
            del e_column[j]

            for index, element in e_column:
                if element == 0:
                    continue
                ielement = -element
                amatrix = AugMatrix(amatrix.__fullmatrix.elementary_operation(index + 1, j + 1, scalar=ielement), amatrix.augindex)
            
            j += 1
        
        return amatrix
        
    def rank(self, index = 0):
        """Returns the rank of the augmented matrix
        \nprovide index 0, 1 to get the rank of full augmented matrix, the first matrix respectively, or an index of 2 to return both.
        """
        reduced =  self.rref()
        ranks = reduced.nonzeros(), reduced.matrix.nonzeros()

        if index == 2:
            return ranks
        try:
            
            return ranks[index]
        except IndexError:
            raise IndexError(f"{index} --> invalid, index with 0 or 1")
        except:
            raise ValueError(f"{index} --> indices must be integers or slices, not {type(index).__name__}")
    
    def elementary_operation(self, i:int, j=None, *, scalar=None, row=True):
        """Perform Elementary operation on the augmented matrix.
        eg.
            >>> matA = Matrix([1, 1, 1], [2, 2, 2], [3, 3, 3])
            >>> matB = Matrix([-1, 2, 0], [3, -2, 1], [1, 1, 2])
            >>> augmatA = AugMatrix(matA, matB)
            >>> augmatA
            AMatrix(
            | 1     1     1 | -1     2     0 |
            | 2     2     2 |  3    -2     1 |
            | 3     3     3 |  1     1     2 |)
            >>> 
        \nTo perform Ri(\u03b1)
            >>> elementary_operation(i, scalar=\u03b1)      # Multiply the ith row by \u03b1
            >>> augmatA.elementary_operation(2, scalar=2)
            AMatrix(
            | 1     1     1 | -1     2     0 |
            | 4     4     4 |  6    -4     2 |
            | 3     3     3 |  1     1     2 |)
            >>>     
        \nFor Ri,j Operation
            >>> elementary_operation(i, j)              # Interchange ith and jth rows
            >>> augmatA.elementary_operation(1, 3)
            AMatrix(
            | 3     3     3 |  1     1     2 |
            | 2     2     2 |  3    -2     1 |
            | 1     1     1 | -1     2     0 |)
            >>> 
        \nAnd for Ri,j(\u03b1) Operation
            >>> elementary_operation(i, j, scalar=\u03b1)   # Multiply jth row by \u03b1 and add to ith row
            >>> augmatA.elementary_operation(1, 2, scalar=2)
            AMatrix(
            | 5     5     5 |  5    -2     2 |
            | 2     2     2 |  3    -2     1 |
            | 3     3     3 |  1     1     2 |)
            >>> 
        \nTo perform column operation i.e. Ci(\u03b1) set the 'row' argument to False
            >>> elementary_operation(i, scalar=\u03b1, row=False)
        \nNote: 'row' and 'scalar' are keyword-only arguments
        """
        return AugMatrix(self.__fullmatrix.elementary_operation(i, j, scalar=scalar, row=row), self.augindex)




# The matrix module functions
def generate_identity_matrix(size):
    """Generates an Identity matrix of any specified size"""
    if size < 1:
        raise ValueError(f"{size} --> Invalid size for Identity Matrix")
    identityMatrix = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    return Matrix(identityMatrix, input_type=1)

def scalar_matrix(shape, scalar):
    """Generates a Scalar matrix of any specified shape and scalar value"""
    if shape < 1:
        raise ValueError(f"{shape} --> Invalid size for Identity Matrix")
    identityMatrix = [[scalar if i == j else 0 for j in range(shape)] for i in range(shape)]
    return Matrix(identityMatrix, input_type=1)

def zero_matrix(shape:tuple):
    """Generates a Zero matrix of any specified size"""
    return Matrix._unitgenerator(0, shape)

def ones_matrix(shape:tuple):
    """Generates a Ones matrix of any specified size"""
    return Matrix._unitgenerator(1, shape)

def constant_matrix(number, shape):
    """Generates a constant matrix (of value 'number') of any specified size"""
    return Matrix._unitgenerator(number, shape)

def elementary_matrix(matrixsize, i, j=None, *, scalar=None, row=True):
    """Generates Elementary matrix of any size.
        \nTo generate elementary matrix Ei(\u03b1) of size 3
        >>> elementary_matrix(3, i, scalar=\u03b1)
        \nFor Ei,j matrix of size 3
        >>> elementary_matrix(3, i, j)
        \nAnd for Ei,j(\u03b1) matrix of size 3
        >>> elementary_matrix(3, i, j, scalar=\u03b1)
        \nTo generate column  identity matrix i.e. Ci(\u03b1) set the 'row' argument to False
        >>> elementary_matrix(3, i, scalar=\u03b1, row=False)
        \nNote: 'row' and 'scalar' are keyword-only arguments
        """
    matrix = generate_identity_matrix(matrixsize)

    return matrix.elementary_operation(i, j, scalar=scalar, row=row)

def random_matrix(lower, upper, shape):
    """Randomly generates a matrix of any specified shape"""
    if not isinstance(shape, tuple):
            raise TypeError (f"{shape} --> Required a tuple of matrix dimension e.g (2,3) for a 2x3 matrix")

    rowsize, columnsize = shape

    if rowsize == 0 or columnsize == 0:
            raise ValueError("row or column size cannot be zero")

    randomMatrix = [[randint(lower, upper) for j in range(columnsize)] for i in range(rowsize)]
    return Matrix(randomMatrix, input_type=1)

def random_constant_matrix(lower, upper, shape):
    """Generates a random constant matrix of any shape"""
    return Matrix._unitgenerator(randint(lower, upper), shape)

def isconstantlist(li, unit=None):
    """Returns True if a container contains same element"""
    if len(li) == 0:
        if unit != None and unit != "":
            return False
        else:
            return True

    if unit == None:
        unit = li[0]
    
    for num in li:
        if num != unit:
            return False
    return True

def inverseof(num, infraction = False):
    """Returns the Multiplicative Inverse of a Matrix or a Number"""
    if isinstance(num, Matrix):
        try:
            return num.inverse(infraction = infraction)
        except ZeroDivisionError:
            return None

    if num == 0:
        return None

    if infraction:
        return Fraction(1, num)
    return 1 / num

def augment_matrix(*matrixrows, augmentedcolumn=None, input_type=0):
    """Creates an Augmented Matrix"""
    return AugMatrix(Matrix(*matrixrows, input_type=input_type), augmentedcolumn)


# Thanks for scrolling down to the end 🙂