 # matrixObj

 A small simple matrix module for basic mathematical matrix operations. Create and make use of _Matrix objects_ in your python codes, perform operations like
 Matrix Addition, Subtration, Multiplication and Scalar Division and other operations like (transpose, co-factor, inverse, minor, determinant, adjoint and elementary operation).

> ## Installation
```sh
pip install matrixObj
```

> ## Project Demo
```
from matrixObj import Matrix
```
You can create a new Matrix instance with any of the *python number objects* (int, float, complex and Fraction) eg.
```
matA = Matrix([5, 3, -1], [3, 5, 9], [0, 5, 2])

matB = Matrix([3.0, 4.5], [2.6, 5.2])

cmplxMat = Matrix([1+2j, 2+1j], [4-4j, 1-2j])

print(matA)
print(matB)
print(cmplxMat)
```
```
Output:
| 5      3      -1|
| 3      5       9|
| 0      5       2|

|3.0    4.5|
|2.6    5.2|

|(1+2j) (2+1j)|
|(4-4j) (1-2j)|
```
with Fraction object, you will have to import it from the fractions module
```
from fractions import Fraction

fracMat = Matrix([Fraction(1,3), Fraction(2,5)], [Fraction(1,2), Fraction(3,27)])

print(fracMat)
```
```
output:

|1/3    2/5|
|1/2    1/9|
```
### Matrix Arithmetic Operations
```
A = Matrix([1, -3, 3], [4, 0, 2])
B = Matrix([4, 6, 0], [3, 0, 5])
C = Matrix([3, -2], [0, 4], [-1, 5])
D = Matrix([1, -3, 3], [4, 0, 2])

sumAB = A + B
productAC = A * C

print(sumAB)
print(productAC)
print(A == D)           # Matrix Equality
```
```
Output:
|5      3       3|
|7      0       7|

| 0      1|
|10      2|

True
```
### Square Matrix Operations
```
matrixA = Matrix([1, 0, 4], [5, 2, 1], [1, 1, 1])

print(matrixA.determinant())    # The determinant of the matrix

print(matrixA.minor())          # The minor of the matrix

print(matrixA.cofactor())       # The Cofactor of the matrix

print(matrixA.inverse(infraction=True)) # Inverse of the matrix returned as a matrix of Fraction object
```
```
Output:
13

|  1      4       3|
| -4     -3       1|
| -8    -19       2|

| 1     -4       3|
| 4     -3      -1|
|-8     19       2|

| 1/13   4/13   -8/13|
|-4/13  -3/13   19/13|
| 3/13  -1/13    2/13|
```
### Elementary Operations
```
mat = Matrix([3, 0, 1], [0, 2, 3], [5, -3, -1])

# Elementary Row operation
print(mat.elementary_operation(2, 3))           # Interchange row 2 and 3

print(mat.elementary_operation(1, scalar=2))    # Multiply row 1 by 2

print(mat.elementary_operation(1, 3, scalar=2)) # Multiply row 3 by 2, add the result to row 1
```
```
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
```
# Elementary Column operation

print(mat.elementary_operation(2, 3, row=False))           # Interchanges column 2 and 3
```
```
| 3      1       0|
| 0      3       2|
| 5     -1      -3|
````

### Modifying the Matrix
After initialization of a Matrix object, you can change, insert new and expand the rows/columns in the matrix eg.
```
mat = Matrix([1, 0, 2], [3, 1, 0])

mat.setrow(1, [5, -3, 2])       # Changes row 1 to [5, -3, 2]
mat.insertrow(2, [3, -3, 1])    # Inserts [3, -3, 1] in the second row
mat.expandrow([2, 5, 5])        # Appends row [2, 5, 5] to the matrix
mat.expandcolumn([4, 5, -4, 0]) # Appends column [4, 5, -4, 0]

print(mat)      # With all the modifications we should now have a 4x4 matrix
```
```
Output:
| 5     -3       2       4|
| 3     -3       1       5|
| 3      1       0      -4|
| 2      5       5       0|

```
###  String Representation
The String Representation of the Matrix object (as can be seen from the examples above). All elements (four H_whitespaced from each other and rightly justified) in each row of the matrix are arranged in between two pipe charater "|" but guess what? You can change the this representation to any other desired representation with **_setrepr()_** method. eg. If your loyalty is to python (^_^) and you prefer to have your matrix represented as python list...
```
# Declear a function that takes exactly one argument and returns a str
# This argument will be the tuple of the matrix rows
# which will be supplied by the matrix class when invoking the function

def newrepr(matrix):
    return str(list(matrix))

Matrix.setrepr(newrepr)

mat = Matrix([4, 5, -1], [0, 1, 3], [5, 2, 7])
print(mat)
```
```
Output:
[[4, 5, -1], [0, 1, 3], [5, 2, 7]]
```
You can do str manipulation on the matrix parameter in the body of your defined function and simply return the desired str representantion for your matrix objects. To change back to the defaul representation, use **_resetrepr()_**

### Other Methods of the Matrix class
- tranpose(): returns the transpose of matrix
- zero_matrix(): generates a zero matrix
- ones_matrix(): generates a ones matrix
- random_matrix(): generates a matrix with random numbers
- generate_identity_matrix(): generates identity matrix

Boolean Methods
- issquare()
- symmetric()
- skew()
- invertible()  etc.