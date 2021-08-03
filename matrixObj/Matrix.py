from fractions import Fraction
import copy
from random import randint

class Matrix:
    """A simple class for basic matrix mathematical operations.
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
    
    def __validate_list(self, list_element:list, mt:str):
        if isinstance(list_element, Matrix):
            raise TypeError (f"{list_element} {type(list_element)} --> {mt} to be inserted must be a one-dimension List object")
        self.__validate_matrix([list_element], mt)

    def __validate_type(self, object, compare_type, operator):
        if not isinstance(object, compare_type):
            raise TypeError (f"'{operator}' not supported between instances of '{Matrix.__name__}' and '{type(object).__name__}'")

    def __isavalidindex(self, index:int, mt:str, raise_exception=False):
        if not isinstance(index, int):
            raise TypeError (f"{index} --> Index must be an int")
        
        size_func_dict = {"row":self.rowsize, "column":self.columnsize}    
        if (index < 1) or (index > size_func_dict[mt]()):
            if not raise_exception:
                return False
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
        inter_matrix = copy.deepcopy(self)

        if mt == 'row':
            row1 = self.getrow(i)
            row2 = self.getrow(j)
            inter_matrix.setrow(i, row2)
            inter_matrix.setrow(j, row1)
        else:
            column1 = self.getcolumn(i)
            column2 = self.getcolumn(j)
            inter_matrix.setcolumn(i, column2)
            inter_matrix.setcolumn(j, column1)
        
        return inter_matrix

    def __multiplybyscalar(self, i, scalar, mt="row"):
        scalar_mul_matrix = copy.deepcopy(self)

        if mt == 'row':
            row = list(self.getrow(i))
            Matrix.multiplyListByScalar(row, scalar)
            scalar_mul_matrix.setrow(i, row)
        else:
            column = list(self.getcolumn(i))
            Matrix.multiplyListByScalar(column, scalar)
            scalar_mul_matrix.setcolumn(i, column)
        
        return scalar_mul_matrix

    def __multiplyandadd(self, i, j, scalar, mt="row"):
        mulandadd_matrix = copy.deepcopy(self)
        
        if mt == 'row':
            rowJ = list(self.getrow(j))
            rowI = self.getrow(i)

            Matrix.multiplyListByScalar(rowJ, scalar)
            resultRow  = Matrix.addListsElements(rowI, rowJ)
            mulandadd_matrix.setrow(i, resultRow)
        
        else:
            columnJ = list(self.getcolumn(j))
            columnI = self.getcolumn(i)

            Matrix.multiplyListByScalar(columnJ, scalar)
            resultColumn  = Matrix.addListsElements(columnI, columnJ)
            mulandadd_matrix.setcolumn(i, resultColumn)
        
        return mulandadd_matrix                

    # Object Attribute Getters and Setters
    def getmatrix(self):
        """Returns the elements of the matrix object as a tuple of list"""
        return tuple(copy.deepcopy(self.__matrix))

    def getrow(self, index:int):
        """Returns a tuple of elements of the ith (index) row of the matrix"""
        if not self.__isavalidindex(index, mt="row"):
            return None
        return tuple(copy.deepcopy(self.__matrix[index - 1]))

    def getcolumn(self, index:int):
        """Returns a tuple of elements of the ith (index) column of the matrix"""
        if not self.__isavalidindex(index, mt="column"):
            return None
        return tuple([row[index - 1] for row in self.__matrix])

    def getelement(self, row_index:int, column_index:int):
        """Returns the element in the specified row and column of the matrix"""
        if not self.__isavalidindex(row_index, mt="row"):
            return None
        if not self.__isavalidindex(column_index, mt="column"):
            return None
        return self.__matrix[row_index - 1][column_index - 1]    

    def rowsize(self) -> int:
        """Returns the number of rows in the matrix"""
        return len(self.__matrix)

    def columnsize(self) -> int:
        """Returns the number of columns in the matrix"""
        return len(self.__matrix[0])

    def dimension(self) -> str:
        """Returns the size of the matrix as str in the format
        'rowxcolumn' e.g 4x4
        """
        return f"{self.rowsize()}x{self.columnsize()}"

    def shape(self):
        """Returns a tuple of the dimension of the matrix: (row, column)"""
        return (self.rowsize(), self.columnsize())

    def setrow(self, row_index:int, row_elements:list) -> None:
        """Set the Elements in the ith row of the matrix, i (row_index) must be between range 1 to rowsize\n
            to expand the rows of the matrix, use expandrow()
        """
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        self.__validate_list(row_elements, mt="row")
        
        self.__matrix[row_index - 1] = row_elements

    def setcolumn(self, column_index:int, column_elements:list) -> None:
        """Set the Elements in the ith column of the matrix, i (column_index) must be between range 1 to columnsize\n
            to expand the column of the matrix, use expandcolumn()
        """
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        self.__validate_list(column_elements, mt="column")

        for i in range(len(column_elements)):
            self.__matrix[i][column_index - 1] = column_elements[i]

    def setelement(self, row_index:int, column_index:int, element) -> None:
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

    def insertrow(self, row_index:int, row_elements:list) -> None:
        """To insert a new row to a specified ith row (row_index) position.
        Row position must be between 1 and the initial rowsize,
        to add more rows after the last row, use expandrow()
        """
        self.__isavalidindex(row_index, mt="row", raise_exception=True)
        self.__validate_list(row_elements, mt="row")

        self.__matrix.insert(row_index - 1, row_elements)

    def insertcolumn(self, column_index:int, column_elements:list) -> None:
        """To insert a new column to a specified ith column position.
        column position must be between 1 and the initial columnsize,
        to add more columns after the last column, use expandcolumn()
        """
        self.__isavalidindex(column_index, mt="column", raise_exception=True)
        self.__validate_list(column_elements, mt="column")

        for i in range(len(column_elements)):
            self.__matrix[i].insert(column_index - 1, column_elements[i])
    
    def removerow(self, row_index):
        """Remove a row from the matrix"""
        self.__isavalidindex(row_index, mt="row", raise_exception=True)

        del(self.__matrix[row_index-1])

    def removecolumn(self, column_index):
        """Remove a column from the matrix"""
        self.__isavalidindex(column_index, mt="column", raise_exception=True)

        for i in range(self.rowsize()):
            del(self.__matrix[i][column_index - 1])

    def expandrow(self, *list_of_rows:list) -> None:
        """To append more rows to the end of the last row in the matrix"""
        rows = list(copy.deepcopy(list_of_rows))
        self.__validate_matrix(rows, mt="row")
        self.__matrix = self.__matrix + rows

    def expandcolumn(self, *list_of_columns:list) -> None:
        """To append more columns to the end of the last column in the matrix"""
        columns = list(copy.deepcopy(list_of_columns))
        self.__validate_matrix(columns, mt="column")

        for i in range(len(columns)):
            for j in range(len(columns[i])):
                self.__matrix[j].append(columns[i][j])

    def copy(self):
        """Make a full copy of the matrix instance"""
        return copy.deepcopy(self) 

    # Magic Methods (Overloading Operators)
    def __default_repr(self) -> str:
        k = [ "|" + "    ".join([str(element).rjust(self.__align) for element in row]) + "|" for row in self.__matrix]
        jstr = "\n".join(k)
        m_str = "\n" + jstr
        return m_str

    def __str__(self) -> str:
        if Matrix.__user_defined_repr_present:
            return Matrix.__user_repr(self.getmatrix())
        return self.__default_repr()

    def __repr__(self) -> str:
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
        self.__validate_type(other, compare_type=Matrix.__tuple_of_supported_types, operator="/")
        divident = [[self.__matrix[i][j] / other for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(divident, input_type=1)

    def rational_division(self, integer:int):
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

    def __pow__(self, other):
        self.__validate_type(other, compare_type=Matrix.__tuple_of_supported_types, operator="**")
        exponent = [[self.__matrix[i][j] ** other for j in range(self.columnsize())] for i in range(self.rowsize())]
        return Matrix(exponent, input_type=1)

    # Other Matrix Operation Methods
    def transpose(self):
        """Returns the transpose of the matrix"""
        transposed = [[self.__matrix[j][i] for j in range(self.rowsize())] for i in range(self.columnsize())]
        return Matrix(transposed, input_type=1)
    
    def determinant(self):
        """Returns the determinant of the matrix (Square Matrix)"""
        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')
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

    def minor(self):
        """Returns the minor of the matrix (Square Matrix)"""
        if not self.issquare():
            raise ValueError ('matrix is not a square matrix')

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

    def cofactor(self):
        """Returns the cofactor of the matrix (Square Matrix)"""
        minor_matrix = self.minor().getmatrix()
        cofactor_matrix = [[(-1)**(i+j+2) * minor_matrix[i][j] for j in range(len(minor_matrix[0]))] for i in range(len(minor_matrix))]
        return Matrix(cofactor_matrix, input_type=1)

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

    # Elementary Operation
    def elementary_operation(self, i:int, j=None, *, scalar=None, row=True):
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
    
    def __isconstantmatrix(self, unit):
        for i in range(self.rowsize()):
            for j in range(self.columnsize()):
                if self.__matrix[i][j] != unit:
                    return False
        return True

    def iszeromatrix(self):
        """Returns True if the matrix is a zero matrix i.e. all elements equals 0"""
        return self.__isconstantmatrix(0)

    def isonesmatrix(self):
        """Returns True if the matrix is a ones matrix i.e. all elements equals 1"""
        return self.__isconstantmatrix(1)
    
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

    def diagonal(self):
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

    def generate_identity_matrix(self, size:int=None):
        """Returns Identity matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns Identity matrix of the same dimension as the matrix instance that invokes the method
        """
        if not size:
            size = self.rowsize()
        return generate_identity_matrix(size)

    def ones_matrix(self, size:tuple=None):
        """Returns Ones matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns Ones matrix of the same dimension as the matrix instance that invokes the method
        """
        if not size:
            size = self.shape()
        return Matrix._unitgenerator(1, size)

    def zero_matrix(self, size:tuple=None):
        """Returns Zero matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns Zero matrix of the same dimension as the matrix instance that invokes the method
        """
        if not size:
            size = self.shape()
        return Matrix._unitgenerator(0, size)

    def constant_matrix(self, number, size:tuple=None):
        """Returns Constant matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns Constant matrix of the same dimension as the matrix instance that invokes the method
        """
        if size == None:
            size = self.shape()   
        return Matrix._unitgenerator(number, size)

    def random_matrix(self, lower:int, upper:int, size:tuple=None):
        """Returns a randomly generated matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns random matrix of the same dimension as the matrix instance that invokes the method
        """
        if not size:
            size = self.shape()
        return random_matrix(lower, upper, size)

    def random_constant_matrix(self, lower:int, upper:int, size:tuple=None):
        """Returns random Constant matrix of dimension 'size'. 
        \nIf size (in int) is not specified, Returns random Constant matrix of the same dimension as the matrix instance that invokes the method
        """
        if not size:
            size = self.shape()
        return Matrix._unitgenerator(randint(lower, upper), size)    
    
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

    # Static Methods
    @staticmethod
    def _unitgenerator(unit, size:tuple):
        """For Generating Matrices with constant values e.g[[3, 3, 3], [3, 3, 3], [3, 3, 3]]
        """
        if not isinstance(size, tuple):
            raise TypeError (f"{size} --> Required a tuple of matrix dimension e.g (2,3) for a 2x3 matrix")
        rowsize, columnsize = size
        unitMatrix = [[unit for j in range(columnsize)] for i in range(rowsize)]
        return Matrix(unitMatrix, input_type=1)

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

# The matrix module functions
def generate_identity_matrix(size:int):
    """Generates an Identity matrix of any specified size"""
    if size < 1:
        raise ValueError(f"{size} --> Invalid size for Identity Matrix")
    identityMatrix = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    return Matrix(identityMatrix, input_type=1)

def zero_matrix(size:tuple):
    """Generates a Zero matrix of any specified size"""
    return Matrix._unitgenerator(0, size)

def ones_matrix(size:tuple):
    """Generates a Ones matrix of any specified size"""
    return Matrix._unitgenerator(1, size)

def constant_matrix(number, size:tuple):
    """Generates a constant matrix (of value 'number') of any specified size"""
    return Matrix._unitgenerator(number, size)

def elementary_matrix(matrixsize:int, i:int, j:int=None, *, scalar:int=None, row:bool=True):
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

def random_matrix(lower:int, upper:int, size:tuple):
    """Randomly generates a matrix of any specified size"""
    if not isinstance(size, tuple):
            raise TypeError (f"{size} --> Required a tuple of matrix dimension e.g (2,3) for a 2x3 matrix")
    rowsize, columnsize = size
    randomMatrix = [[randint(lower, upper) for j in range(columnsize)] for i in range(rowsize)]
    return Matrix(randomMatrix, input_type=1)

def random_constant_matrix(self, lower:int, upper:int, size:tuple):
    """Generates a random constant matrix of any size"""
    return Matrix._unitgenerator(randint(lower, upper), size)    