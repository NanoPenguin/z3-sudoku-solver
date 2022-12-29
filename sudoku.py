from z3 import *
from itertools import product

# Print the sudoku board
def print_board(board):
    for i, line in enumerate(board):
        if not i % 3:
            print("#"*13)
        print("#"+"".join([str(x) for x in line[:3]]), end="")
        print("#"+"".join([str(x) for x in line[3:6]]), end="")
        print("#"+"".join([str(x) for x in line[6:9]])+"#")
    print("#"*13)

# Initialize solver
s = Solver()

# Generate the matrix of variables
v = []
for a in range(9):
    v.append(Ints(" ".join([f"i{a}{b}" for b in range(9)])))

for a, b in product(range(9), repeat=2):
    # Set the range of the integers to 0-9
    s.add(1 <= v[a][b])
    s.add(v[a][b] <= 9)

    # Set constraints that no row or column can have duplicates
    for c in range(9):
        if b != c:
            s.add(v[a][b] != v[a][c])
            s.add(v[b][a] != v[c][a])

# Set contraint that no box can have duplicates
for a, b, c, d, e, f in product(range(3), repeat=6):
    if c != e and d != f:
        s.add(v[a*3+c][b*3+d] != v[a*3+e][b*3+f])

print("Enter contraints as \"X Y Value\", then press enter.")

# Get given tiles
while True:
    indata = input("> ")
    if not len(indata): break
    x, y, value = indata.split()
    x = int(x)
    y = int(y)
    value = int(value)
    s.add(v[y-1][x-1] == value)

try:
    # Run solver
    s.check()

    # Get results
    m = s.model()

    # Generate board
    board = []
    for a in range(9):
        board.append([m[v[a][b]] for b in range(9)])

    # Print board
    print()
    print_board(board)

except:
    print("Could not solve constraints")
