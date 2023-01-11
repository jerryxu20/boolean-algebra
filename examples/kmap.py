from BoolAlg import BoolBin

# I am given a function as sum of minterms
bb = BoolBin()
minterms = [0, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14, 15]
bb.kmap(4, minterms, 'cd', 'ab')

#              ab       
#        00  01  11  10
#    00| 1 | 0 | 1 | 1 |
#    01| 0 | 1 | 0 | 1 |
# cd 11| 1 | 1 | 1 | 0 |
#    10| 1 | 1 | 1 | 1 |

# I am given W(K, L, M, U) = K'LM'U' + K'LM'U + KL'M'U + KLMU + K'L'MU which I turn into a python function
def W(K, L, M, U):
    return ((not K and L and not M and not U)
            or (not K and L and not M and U)
            or (K and not L and not M and U)
            or (K and L and M and U)
            or (not K and not L and M and U))
    
# Variables are given in same order as they appear in the arguments of W.
# I am able to change what variables are grouped together
bb.f_kmap(W, ['K', 'L', 'M', 'U'], ['K', 'L'], ['M', 'U'])
bb.f_kmap(W, ['K', 'L', 'M', 'U'], ['U', 'K'], ['M', 'L'])
# W:
#              KL       
#        00  01  11  10
#    00| 0 | 1 | 0 | 0 |
#    01| 0 | 1 | 0 | 1 |
# MU 11| 1 | 0 | 1 | 0 |
#    10| 0 | 0 | 0 | 0 |
#
# W:
#              UK       
#        00  01  11  10
#    00| 0 | 0 | 1 | 0 |
#    01| 1 | 0 | 0 | 1 |
# ML 11| 0 | 0 | 1 | 0 |
#    10| 0 | 0 | 0 | 1 |