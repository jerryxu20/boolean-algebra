from BoolAlg import WeightedSum

# With weighted code of 6, 2, 1, 1 can I cover all digits 1 to 9?
weights = [6, 2, 1, 1]
ws = WeightedSum(weights)

for i in range(10):
    if ws.is_covered(i):
        print(f"{i} is covered")
        continue
    print(f"{i} is not covered")

# Or I could do

if ws.max_continous_coverage() >= 9:
    print("it's possible")
else:
    print("not possible")

# 0 is covered
# 1 is covered
# 2 is covered
# 3 is covered
# 4 is covered
# 5 is not covered
# 6 is covered
# 7 is covered
# 8 is covered
# 9 is covered

# Provide all representations for the decimal numbers
for num, value in ws.rep.items():
    print(num, value)

# 0 ['0000']
# 1 ['0001', '0010']
# 2 ['0011', '0100']
# 3 ['0101', '0110']
# 4 ['0111']
# 6 ['1000']
# 7 ['1001', '1010']
# 8 ['1011', '1100']
# 9 ['1101', '1110']
# 10 ['1111']

# These questions really annoy me because they ask for a justification
# What they expect is brute force but it can be done faster