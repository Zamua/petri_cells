# this is not yet tested

import random
from cross_react_programs import cross_react_programs

LENGTH = 50
WIDTH = 50
MAX_EPOCHS = None

board = [[chr(0)]*LENGTH]*WIDTH
ordered_pairs = [(a, b) for a in range(WIDTH) for b in range(WIDTH)]
print(ordered_pairs)

epoch = 0
while MAX_EPOCHS is None or epoch < MAX_EPOCHS:
    random.shuffle(ordered_pairs)
    visited = [[False] * LENGTH] * WIDTH
    for op in ordered_pairs:
        if visited[op[0]][op[1]]:
            continue
        neighbor_x = op[0] + random.randint(-2, 2)
        neighbor_y = op[1] + random.randint(-2, 2)
        old_program = board[op[0]][op[1]]
        old_neighbor_program = board[neighbor_x][neighbor_y]
        new_program, new_neighbor_program = cross_react_programs(old_program, old_neighbor_program)
        board[op[0]][op[1]] = new_program
        board[neighbor_x][neighbor_y] = new_neighbor_program
    epoch += 1

