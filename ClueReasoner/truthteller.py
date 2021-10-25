from SATSolver import *

clauses = [[-1,3], [-1,1], [-2,-3], [-3,2], [-3,1], [-1,-3], [3,-2]]
print("Is Cal a truth-teller?")
result = testLiteral(3, clauses)

if result == True:
    print("Cal is a liar.")
    print("Amy is a liar.")
    print("Bob is not a liar.")
elif result == False:
    print("Cal is not a liar.")
    print("Amy is a liar.")
    print("Bob is a liar.")
else:
    print("Unknown")