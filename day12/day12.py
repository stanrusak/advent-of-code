import pytest

TEST_DATA = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 31, 29

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    grid = data.splitlines()
    
    start, end, grid =  get_grid(data)
    part1 = get_shortest_path(start, end, grid)

    min_steps = part1
    for r, row in enumerate(grid):
        for c, height in enumerate(row):

            if height == 97:
                
                try:
                    steps = get_shortest_path((r,c), end, grid, step_limit=min_steps)
                    min_steps = min(steps,min_steps)
                except BoredCountingStepsError:
                    continue
    
    part2 = min_steps

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_grid(data):

    grid = []
    for r, row in enumerate(data.splitlines()):

        grid_row = []
        for c, char in enumerate(row):
            
            if char == 'S':
                start = (r, c)
                grid_row.append(ord('a'))
            
            elif char == 'E':
                end = (r, c)
                grid_row.append(ord('z')) 
            else:
                grid_row.append(ord(char))
        
        grid.append(grid_row)

    return start, end, grid

def get_shortest_path(start, end, grid,step_limit=10000):

    exploring = [[start]]
    seen = set()
    steps = -1

    while steps <= step_limit:

        steps += 1
        batch = exploring.pop(0)
        next_batch = set()

        for r, c in batch:        
            
            seen.add((r,c))

            if (r, c) == end:
                return steps

            limit = grid[r][c] + 1
            if r - 1 >= 0 and grid[r-1][c] <= limit and (r-1,c) not in seen:
                next_batch.add((r-1,c))
            
            if c - 1 >= 0 and grid[r][c-1] <= limit and (r,c-1) not in seen:
                next_batch.add((r,c-1))
            
            if r + 1 < len(grid) and grid[r+1][c] <= limit and (r+1,c) not in seen:
                next_batch.add((r+1,c))
            
            if c + 1 < len(grid[r]) and grid[r][c+1] <= limit and (r,c+1) not in seen:
                next_batch.add((r,c+1))
        
        exploring.append(next_batch)

    raise BoredCountingStepsError("Too many steps, bored now...")

class BoredCountingStepsError(Exception):
    pass

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