from BoolAlg import MTerm, BoolBin
bb = BoolBin()

# I want to write F(X, W, Z, V) = (X + W + Z' + XWZ') (X + W'Z + XWZ) (X + V + XVW)
# as sum of minterms
def F(X, W, Z, V):
    return (
        (X or W and not Z or X and W and not Z) or
        (X and not W and Z or X and W and Z) or
        (X or V or X and V and W)
    )
    
minterms = bb.terms(4, F, 'min')
print(minterms)
# [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15]


# Now I am given a functions as product of maxterms and want to get the logical expression before simplifying
# G(A, B, C) = prouduct Max (1, 3, 5, 7)
terms = [1, 3, 5, 7]
m = MTerm(['A', 'B', 'C'], )

# Gives POS form
m.expand_max(terms)
# Gives SOP form. I also gave the function a name.
m.expand_max(terms, min=True, f='G')

# f(A,B,C) = 
# (A + B + C') (A + B' + C') (A' + B + C') (A' + B' + C') 
# G(A,B,C) = 
# (A + B + C) (A + B' + C) (A' + B + C) (A' + B' + C) 

# Then I might find it simplifies to C'. To check this
def G(A, B, C):
    return (
        (A or B or not C) and
        (A or not B or not C) and
        (not A or B or not C) and
        (not A or not B or not C)
    )

def g(A, B, C):
    return not C

bb.truth_table(3, G, g, rep="bits", check_equal=True)
# Truth Table:
# abc  G g Assert
# 000  1 1 1
# 001  0 0 1
# 010  1 1 1
# 011  0 0 1
# 100  1 1 1
# 101  0 0 1
# 110  1 1 1
# 111  0 0 1