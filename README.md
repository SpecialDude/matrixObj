# **matrixObj**

 A simple matrix module for basic mathematical matrix operations. Create and make use of _Matrix objects_ in your python codes, perform operations like
 Matrix Addition, Subtration, Multiplication and Scalar Division and other operations like (transpose, co-factor, inverse, minor, determinant, adjoint and elementary operation).

> ## Installation

```sh
pip install matrixObj
```

> ## Project Demo

```py
from matrixObj import Matrix
```

You can create a new Matrix instance with any of the *python number objects* (int, float, complex and Fraction) eg.

```py
matA = Matrix([5, 3, -1], [3, 5, 9], [0, 5, 2])

matB = Matrix([3.0, 4.5], [2.6, 5.2])

cmplxMat = Matrix([1+2j, 2+1j], [4-4j, 1-2j], [3+0j, 1j])

print(matA,  end="   ")
print(matA.dimension() + " Matrix")     # dimension() returns the string depicting the matrix's shape.

print(matB, end="   ")
print(matB.dimension() + " Matrix")

print(cmplxMat, end="   ")
print(cmplxMat.dimension() + " Matrix")
```

```bat
Output:

| 5     3    -1|
| 3     5     9|
| 0     5     2|   3x3 Matrix

|3.0    4.5|
|2.6    5.2|   2x2 Matrix

|(1+2j)    (2+1j)|
|(4-4j)    (1-2j)|
|(3+0j)        1j|   3x2 Matrix
```

with Fraction object, you will have to import it from the fractions module

```py
from fractions import Fraction

fracMat = Matrix(
    [Fraction(1,3), Fraction(2,5)],
    [Fraction(1,2), Fraction(3,27)]
    )

print(fracMat)
```

```bat
output:

|1/3    2/5|
|1/2    1/9|
```

### **Matrix Arithmetic Operations**

```py
A = Matrix([1, -3, 3], [4, 0, 2])
B = Matrix([4, 6, 0], [3, 0, 5])
C = Matrix([3, -2], [0, 4], [-1, 5])
D = Matrix([1, -3, 3], [4, 0, 2])
E = Matrix([3, 1, 0], [9, -1, 2], [0, 1, 3])


# Addition and Subtraction
sumAB = A + B           # Sum of matrices
difAB = A - B           # Difference of matrices


# Product
productAC = A * C       # Product of matrices

# Scalar Division
a = A / 2               # Same operation as (A * 0.5)

print(sumAB, "--> A + B")
print(difAB, "--> A - B")
print(productAC, "--> A * C")
print(a, "--> A \u00F7 2")          # Unicode of Division Symbol (\u00F7)
print("\nA == D:", A == D)          # Matrix Equality

```

```bat
Output:

|5    3    3|
|7    0    7| --> A + B

|-3    -9     3|
| 1     0    -3| --> A - B

| 0     1|
|10     2| --> A * C

| 0.5    -1.5     1.5|
| 2.0     0.0     1.0| --> A ÷ 2

A == D: True
```

### **Square Matrix Operations**

```py
matrixA = Matrix([4, 8, 2], [0, 5, 2], [4, 8, 1])

print(matrixA.determinant())    # The determinant of the matrix

print(matrixA.minor())          # The minor of the matrix

print(matrixA.cofactor())       # The Cofactor of the matrix

print(matrixA.inverse())        # Inverse of the matrix
```

```bat
Output:

-20

|-11     -8    -20|
| -8     -4      0|
|  6      8     20|

|-11      8    -20|
|  8     -4      0|
|  6     -8     20|

|0.55    -0.4    -0.3|
|-0.4     0.2     0.4|
| 1.0    -0.0    -1.0|
```

To return the inverse of the matrix in fraction, set the argument **_infraction=True_**

```py
print(matrixA.inverse(infraction=True))
```

```bat
Output:

|11/20     -2/5    -3/10|
| -2/5      1/5      2/5|
|    1        0       -1|
```

To get minor and co-factor at a particular ith, jth position of the matrix, use the methods ***minor_at_ij()*** and ***cofactor_at_ij()*** (i and j positions are indexed from 1 instead of 0) eg.

```py
print(matrixA.minor_at_ij(1, 1))      # Minor at row 1 column 1

print(matrixA.cofactor_at_ij(3, 1))   # Cofactor at row 3 column 1 
```

```bat
Output:

-11
6
```

### More Square matrix arithmetic operations

```py
A = Matrix([4, 8, 2], [0, 5, 2], [4, 8, 1])
B = Matrix([3, 7, 0], [2, 9, 7], [-1, -3, 0])

# Power of a Square Matrix
print( A ** 3 )                 # A³  = A * A * A
print( A ** -1)                 # A⁻¹ = A.inverse(infraction=True)
print( A ** -2)                 # A⁻² = A.inverse(infraction=True) ** 2

# Division of Square 
print(2 / A)                    # 2 * A.inverse(infraction)
print( A / B)                   # A * B
print(A / A)                    # Identity Matrix
```

```bat
Output:

|200    840    250|
| 80    365    110|
|180    760    225|

|11/20     -2/5    -3/10|
| -2/5      1/5      2/5|
|    1        0       -1|

|13/80    -3/10    -1/40|
| 1/10      1/5     -1/5|
|-9/20     -2/5     7/10|

|11/10     -4/5     -3/5|
| -4/5      2/5      4/5|
|    2        0       -2|

|  17/7       2/7      27/7|
|-29/14       2/7    -79/14|
| 31/14       1/7     41/14|

|1    0    0|
|0    1    0|
|0    0    1|
```

### **Elementary Operations**

```py
mat = Matrix([3, 0, 1], [0, 2, 3], [5, -3, -1])

# Elementary Row operation
print(mat.elementary_operation(2, 3))           # Interchange row 2 and 3

print(mat.elementary_operation(1, scalar=2))    # Multiply row 1 by 2

print(mat.elementary_operation(1, 3, scalar=2)) # Multiply row 3 by 2, add the result to row 1
```

```bat
Output:

| 3      0       1|
| 5     -3      -1|
| 0      2       3|

| 6      0       2|
| 0      2       3|
| 5     -3      -1|

|13     -6      -1|
| 0      2       3|
| 5     -3      -1|
```

For Elementary column Operation set argument row=False eg.

```py
# Elementary Column operation

print(mat.elementary_operation(2, 3, row=False))           # Interchanges column 2 and 3
```

```bat
Output:

| 3      1       0|
| 0      3       2|
| 5     -1      -3|
```

### Row Reducing to Echelon Form

To row reduce matrix to echelon form by means of elementary operations, call the method **_rref()_** on the matrix eg.

```py
# Reducing Matrix to echelon form

a = Matrix([1, 0, -2], [2, -1, 3], [4, 1, 8])
reduced_a = a.rref()

print("Matrix a")
print(a)
print("\nReduced matrix a")
print(reduced_a)

b = Matrix([0, 1, 3], [4, 2, -8], (2, 3, 2))
reduced_b = b.rref()

print("\n\nMatrix b")
print(b)
print("\nReduced matrix b")
print(reduced_b)

print("\nThe Rank of matrix a is:", a.rank())
print("The Rank of matrix b is:", b.rank())
```

```bat
Output:

Matrix a

| 1     0    -2|
| 2    -1     3|
| 4     1     8|

Reduced matrix a

|1.0    0.0    0.0|
|0.0    1.0    0.0|
|0.0    0.0    1.0|


Matrix b

| 0     1     3|
| 4     2    -8|
| 2     3     2|

Reduced matrix b

| 1.0     0.0    -3.5|
|   0       1       3|
| 0.0     0.0     0.0|

The Rank of matrix a is: 3
The Rank of matrix b is: 2
```

By default, the _**rref()**_ method returns the reduced matrix in floating numbers, to perform the reduction operation in fraction set the argument **infraction** to **True**

```py
print(b.rref(infraction=True))
```

```bat
Output:

|   1       0    -7/2|
|   0       1       3|
|   0       0       0|
```

### Reducing to Upper and Lower Triangular Matrix

Reduce square matrices to upper or lower triangular matrices. eg,

```py
>>> import matrixObj
>>> 
>>> matrix = matrixObj.random_matrix(-10, 15, (3, 3))
>>> # Generates a random matrix of size 3 (with random numbers between -10 and 15)
>>> 
>>> matrix
Matrix(
|-5    -7    11|
| 9    15     6|
| 5    15    -3|)
>>> 
>>> matrix.reduce_to_utriangle() # Reduce to upper triangle matrix
Matrix(
|   -5       -7       11|
|    0     12/5    129/5|
|    0        0      -78|)
>>> 
>>> matrix.reduce_to_ltriangle() # Reduce to lower triangle matrix
Matrix(
|-104/15          0          0|
|     19         45          0|
|      5         15         -3|)
>>> 
```
If matrix is not a square matrix and the row size is less than the column size, reducing to triangular matrix returns an AugMatrix (the extra columns are augmented), otherwise (i.e rowsize > columnsize), raises ValueError

```py
>>> matrix = matrixObj.random_matrix(-8, 8, (3, 4))
>>> matrix
Matrix(
|3    6    4    8|
|8    4    2    6|
|3    5    0    2|)
>>> 
>>> matrix.reduce_to_ltriangle()
AMatrix(
|-59/2        0        0 |    -8 |
| 13/2        1        0 |     2 |
|    3        6        4 |     8 |)
>>> 
```

### **Modifying the Matrix**

After initialization of a Matrix object, you can change, insert new and expand the rows/columns in the matrix eg.

```py
mat = Matrix([1, 0, 2], [3, 1, 0])

mat.setrow(1, [5, -3, 2])       # Changes row 1 to [5, -3, 2]
mat.insertrow(2, [3, -3, 1])    # Inserts [3, -3, 1] in the second row
mat.expandrow([2, 5, 5])        # Appends row [2, 5, 5] to the matrix
mat.expandcolumn([4, 5, -4, 0]) # Appends column [4, 5, -4, 0]

print(mat)      # With all the modifications we should now have a 4x4 matrix
```

```bat
Output:
| 5     -3       2       4|
| 3     -3       1       5|
| 3      1       0      -4|
| 2      5       5       0|

```

#### **Modifying by Slicing**

Get, set or delete part/slice of the matrix. eg.

```py
# Getting part/slice of the matrix
matA = Matrix([2, 5, -4], [4, 5, 9], [-1, -8, 0], [7, 0, 5])

print(matA[1, 0])           # Gets first element in the second row 

print(matA[2])              # Gets the third row of the matrix

print(matA[:, -1])          # Gets the last column of the matrix 

print(matA[0:3])            # Gets the first, the second and the third row

print(matA[::-1, ::-1])     # Gets the reverse of the matrix rows with each row also reversed

```

```bat
Output:
4

|-1    -8     0|

|-4     9     0     5|

| 2     5    -4|
| 4     5     9|
|-1    -8     0|

| 5     0     7|
| 0    -8    -1|
| 9     5     4|
|-4     5     2|
```

```py
# Setting part/slice of the matrix
matA[1] = [-20, 40, 10]     # sets the second row
print(matA)

matA[:, 0] = [1, 2, 3, 4]   # sets the first column
print(matA)
```

```bat
Output:

|  2      5     -4|
|-20     40     10|
| -1     -8      0|
|  7      0      5|

|  1      5     -4|
|  2     40     10|
|  3     -8      0|
|  4      0      5|
```

All elements in a slice can be set to the same scalar value eg.

```py
matA[-1] = 4        # Sets all the elements in the last row to 4
print(matA)

from fractions import Fraction
matA[:] = Fraction(1, 3)    # Sets all elements in the matrix to 1/3
print(matA)
```

```bat
Output:
| 2     5    -4|
| 4     5     9|
|-1    -8     0|
| 4     4     4|

|1/3    1/3    1/3|
|1/3    1/3    1/3|
|1/3    1/3    1/3|
|1/3    1/3    1/3|
```

Using the __*del()*__ function to delete some part of the matrix, this can only delete complete row(s) or column(s)...

```py
matA = Matrix([2, 5, -4], [4, 5, 9], [-1, -8, 0], [7, 0, 5])
```

```py
del(matA[1])            # Deletes the second row
print(matA)
```

```bat
Output:

| 2     5    -4|
|-1    -8     0|
| 7     0     5|
```

```py
del(matA[:, 0])         # Deletes the first column
print(matA)
```

```bat
Output:

| 5    -4|
| 5     9|
|-8     0|
| 0     5|
```

```py
del(matA[1:-1]) # Deletes the second row up to the last row
print(matA)
```

```bat
Output:

| 2     5    -4|
| 7     0     5|
```

```py
from matrixObj import random_matrix
matB = random_matrix(-10, 10, (4, 6))
print(matB)
del(matB[:, -1:0:-2]) # Deletes columns 6, 4, and 2
print(matB)
```

```bat
Output:

|-10      0     -5     -9      7     -3|
|  4     -8     -4     -7      9      3|
| -1      9      8     -7      2     -5|
|  2      4      5     -1     -6     -1|

|-10     -5      7|
|  4     -4      9|
| -1      8      2|
|  2      5     -6|
```

**_NOTE_**: Using the methods (_**insertrow()**_, _**insertcolumn()**_, _**expandrow()**_, _**removerow()**_ etc.) to modify matrix take indexes from 1 instead of slicing which takes indexes from 0

### **String Representation**

The String Representation of the Matrix object (as can be seen from the examples above). All elements (four H_whitespaced from each other and rightly justified) in each row of the matrix are arranged in between two pipe charater "|" but guess what? You can change the representation to any other desired representation with **_setrepr()_** method. eg. If you prefer to have your matrix represented as python list, consider the example below:

```py
# Declear a function that takes exactly one argument and returns a str
# This argument will be the tuple of the matrix rows
# which will be supplied by the matrix class when invoking the function

def newrepr(matrix):
    return str(list(matrix))

Matrix.setrepr(newrepr)

mat = Matrix([4, 5, -1], [0, 1, 3], [5, 2, 7])
print(mat)
```

```bat
Output:
[[4, 5, -1], [0, 1, 3], [5, 2, 7]]
```

You can do str manipulation on the matrix parameter in the body of your defined function and simply return the desired str representantion for your matrix objects. To change back to the defaul representation, use **_resetrepr()_**

> ## **Augmented Matrix**

A subclass of the Matrix class. Append the columns of two matrix to form an augmented matrix and perform the same elementary operations on both matrices augmented together.
The constructor takes two arguments (matrix A and matrix B) which can be matrix objects or a list of matrix rows of both matrices

```py
>>> from matrixObj import AugMatrix
>>> 
>>> 
>>> matA = Matrix([3, 5, 9], [1, -2, 0], [2, 3, 1])
>>> b = [4, -5, 7]
>>> augmentAB = AugMatrix(matA, augcolumn=b)
>>> augmentAB
AMatrix(
| 3     5     9 |  4 |
| 1    -2     0 | -5 |
| 2     3     1 |  7 |)
>>> 

# Augmented Matrix from two matrices

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

# If a second matrix is not supplied, the first matrix is augmented with it's last column as the augmented part

>>> c = Matrix([-2, 3, 1, 5], [3, 0, 9, 2], [1, 2, 9, 0])
>>> augC = AugMatrix(c)
>>> augC
AMatrix(
|-2     3     1 |  5 |
| 3     0     9 |  2 |
| 1     2     9 |  0 |)
>>> 

#If a second integer argument is suppied, the first matrix is augmented by indexing from the integer argument

>>> d = Matrix([4, 5, 0, 1, -1], [-2, 2, 1, 3, -1], [3, 7, 0, -5, 2])
>>> augD = AugMatrix(d, 3)
AMatrix(
| 4     5     0 |  1    -1 |
|-2     2     1 |  3    -1 |
| 3     7     0 | -5     2 |)
>>>
```

### **Solving System of linear Equation**

Suppose there's a system of linear equations which may be consistent with unique solution or many solutions or inconsistent with no solution. e.g.

```tex
Consistent Equations with Unique Solution
        1                       2
2x + y  -  z = 1         a + 2b +  c = 2
   + 2y +  z = 2        3a +  b - 2c = 1
5x + 2y - 3z = 3        4a - 3b -  c = 3
```

```py
#                       1

# 2x + y  -  z = 1
#    + 2y +  z = 2
# 5x + 2y - 3z = 3 

# to matrix
coeficients = Matrix(   [2, 1, -1],
                        [0, 2, 1],
                        [5, 2, -3]  )

constants = Matrix( [1],
                    [2],
                    [3] )

augEquation = AugMatrix( coeficients, constants )
reducedEquation = augEquation.rref(infraction=True)
solution = reducedEquation.augcolumn
print(augEquation)
print(reducedEquation)
print(solution)

print(f"\nx = {solution[0, 0]}")
print(f"y = {solution[1, 0]}")
print(f"z = {solution[2, 0]}")

```

```bat
Output:

| 2     1    -1 |  1 |
| 0     2     1 |  2 |
| 5     2    -3 |  3 |

| 1     0     0 | -3 |
| 0     1     0 |  3 |
| 0     0     1 | -4 |

|-3|
| 3|
|-4|

x = -3
y = 3
z = -4
```

```py
#                       2
#  a + 2b +  c = 2
# 3a +  b - 2c = 1
# 4a - 3b -  c = 3

coeficients = Matrix(   [1, 2, 1],
                        [3, 1, -2],
                        [4, -3, -1] )
constants = Matrix( [2],
                    [1],
                    [3] )

equations = AugMatrix( coeficients, constants )
reducedEquation = equations.rref(infraction=True)
solution = reducedEquation.augcolumn

print(equations)
print(solution)

print(f"\na = {solution[0, 0]}, b = {solution[1, 0]}, c = {solution[2, 0]}")
```

```bat
Output:

| 1     2     1 |  2 |
| 3     1    -2 |  1 |
| 4    -3    -1 |  3 |

|1|
|0|
|1|

a = 1, b = 0, c = 1

```

This type of equation can also be solved algebraically or using Cramer's Rule

```tex
                       2
  a + 2b +  c = 2
 3a +  b - 2c = 1
 4a - 3b -  c = 3

In Matrix

[1    2    1]           [a]             [2]
[3    1   -2]     x     [b]     =       [1]
[4   -1   -1]           [c]             [3]

      A           x      B      =        C

Algebraically:

A x B = C   -->   B = C / A     -->    B = A⁻¹ x C

Using Cramer's Rule (Bᵢ = |Aᵢ| ÷ |A|)

a = |A₁| ÷ |A|
b = |A₂| ÷ |A|
c = |A₃| ÷ |A|
```

```py
# Algebraically

A = Matrix([1, 2, 1], [3, 1, -2], [4, -1, -1])
C = Matrix([2], [1], [3])

B = (A ** -1) * C
print(B)

print(f"\nB = {[int(i) for i in B.getcolumn(1)]}")

# By Cramer's Rule
print("\nUsing Cramer's Rule")
det = A.determinant()           # Determinant of Matrix A

# Value of a
Acopy = A.copy()                # Making a copy of Matrix A
Acopy[:, 0] = C                 # Modifying Matrix, seting column 1 of A to C
a = Acopy.determinant() / det
print(f"a = {a}")

# Value of b
Acopy = A.copy()
Acopy[:, 1] = C                 # Modifying Matrix, seting column 2 of A to C
b = Acopy.determinant() / det
print(f"b = {b}")

# Value of c
Acopy = A.copy()
Acopy[:, 2] = C                 # Modifying Matrix, seting column 3 of A to C
c = Acopy.determinant() / det
print(f"c = {c}")
```

```bat
Output: 

|1|
|0|
|1|

B = [1, 0, 1]

Using Cramer's Rule
a = 1.0
b = -0.0
c = 1.0
```

### **Other Methods of the Matrix class**

- tranpose(): returns the transpose of matrix
- nonzeros(): returns the number non-zero rows/columns in matrix
- sum(): returns the sum of all elements in matrix
- identity(): generates identity matrix
- zero_matrix(): generates a zero matrix
- ones_matrix(): generates a ones matrix
- random_matrix(): generates a matrix with random numbers
- trace(): returns the sum of the diagonal elements

Boolean Methods

- issquare()
- symmetric()
- skew()
- invertible()
- isorthogonal()
- isnormal()
- isrowmatrix()
- iscolumnmatrix()
- issingletonmatrix()
- isnull()