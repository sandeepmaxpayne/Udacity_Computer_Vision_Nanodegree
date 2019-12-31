import pdb
from helpers import normalize, blur

def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1.0 / area
    beliefs = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color, grid, beliefs, p_hit, p_miss):
    new_beliefs = []
    normalize_new_belief = []

    #
    # TODO - implement this in part 2
    height = len(beliefs)
    width = len(beliefs[0])
    
    for i in range(height):
        row = []
        for j in range(width):
            belief = beliefs[i][j]
            if color == grid[i][j]:
                row.append(belief * p_hit)
            else:
                row.append(belief * p_miss)
        new_beliefs.append(row)
        
       
    total = 0
    for i in range(height):
        for j in range(width):
            total += new_beliefs[i][j]
        
       
    #Normalisation
    for i in range(height):
        row = []
        for j in range(width):
            row.append(new_beliefs[i][j] / total)
        normalize_new_belief.append(row)
    
        
        
    #

    return normalize_new_belief

## was bug and solved
def move(dy, dx, beliefs, blurring):
    height = len(beliefs)
    width = len(beliefs[0])
    new_G = [[0.0 for i in range(width)] for j in range(height)]
    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            new_i = (i + dy ) % height
            new_j = (j + dx ) % width
            # pdb.set_trace()
            pdb.set_trace()
            new_G[int(new_i)][int(new_j)] = cell
    return blur(new_G, blurring)