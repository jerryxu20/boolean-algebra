from BoolAlg import BoolBin

bb = BoolBin()

# I am given a function F(A, B, C) = A(B + C') + C(A' + B)
# Once I simplify I get F(A, B, C) = A + C
# To check if I was correct I write theses two functions out in python and print the truth tables

def unsimplified(A, B, C):
    return (A and (B or not C)) or (C and (not A or not B))

def simplified(A, B, C):
    return A or C

# Pass in as many functions as you'd like through *args
bb.truth_table(3, unsimplified, simplified, vars=['A', 'B', 'C'], rep="bits", check_equal=True)

# Truth Table:
# ABC  unsimplified  simplified    Assert
# 000  0             0             1
# 001  1             1             1
# 010  0             0             1
# 011  1             1             1
# 100  1             1             1
# 101  1             1             1
# 110  1             1             1
# 111  1             1             1

# Or using True/False instead of 1/0. Could also use T/F with rep="short"
bb.truth_table(3, unsimplified, simplified, vars=['A', 'B', 'C'], rep="boolean")
