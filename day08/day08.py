import pytest
import numpy as np
from time import perf_counter

TEST_DATA = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21, 8

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):
    
    grid = [[int(i) for i in row] for row in data.splitlines()]
    part1, part2 = compute_solution(grid)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def compute_solution(grid):

    size = len(grid)

    invisible = 0
    max_scenic_score = 0
    for i in range(1,size-1):
        for j in range(1, size-1):
        
            invisible_directions, (left, right, up, down) = get_visibility(grid, i, j)
            if invisible_directions == 4:
                invisible += 1
            
            scenic_score = left * right * up * down
            max_scenic_score = max(max_scenic_score, scenic_score)
    
    visible = size ** 2 - invisible

    return visible, max_scenic_score

def get_visibility(grid, i, j):
    
    left = look_left(grid, i, j)
    right = look_right(grid, i, j)
    up = look_up(grid, i, j)
    down = look_down(grid, i, j)

    invisible_directions = 0
    if left != j:
        invisible_directions += 1
        left += 1
        
    if right != len(grid) - j - 1:
        invisible_directions += 1
        right += 1
        
    if up != i:
        invisible_directions += 1
        up += 1
    
    if down != len(grid) - i - 1:
        invisible_directions += 1
        down += 1

    return invisible_directions, (left, right, up, down) 

def look_left(grid, i, j):
    
    visible = 0
    for jj in range(0, j):
        if grid[i][j-jj-1] < grid[i][j]:
            visible += 1 
        else:
            break
    
    return visible

def look_right(grid, i, j):
    
    visible = 0
    for jj in range(j+1, len(grid)):
        if grid[i][jj] < grid[i][j]:
            visible += 1 
        else:
            break
    
    return visible

def look_up(grid, i, j):
    
    visible = 0
    for ii in range(0, i):
        if grid[i-ii-1][j] < grid[i][j]:
            visible += 1 
        else:
            break
    
    return visible

def look_down(grid, i, j):
    
    visible = 0
    for ii in range(i+1, len(grid)):
        if grid[ii][j] < grid[i][j]:
            visible += 1 
        else:
            break
    
    return visible

@pytest.mark.parametrize(
    ('input_data','output'),
    (
        (TEST_DATA, EXPECTED),
    )
)
def test_main(input_data, output):
    assert main(input_data) == output

if __name__ == "__main__":
    main(data)