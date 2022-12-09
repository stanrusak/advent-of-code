import pytest
from collections import defaultdict

TEST_DATA1 = "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"
TEST_DATA2 = "R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20\n"
EXPECTED1 = 13, 1
EXPECTED2 = 88, 36

DIRS = {"R": 1, "L": -1, "U": 1j, "D": -1j}

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    moves = [(line.split()[0], int(line.split()[1])) for line in data.splitlines()]

    knots = 1
    visited = move(moves,knots)
    part1 = len(visited.values())
    
    knots = 9
    visited = move(moves, knots) 
    part2 = len(visited.values())

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def move(moves, N):

    origin = 0 + 0j
    visited = defaultdict(int)
    visited[origin] += 1

    rope = {i: origin for i in range(0,N+1)}
    
    for d, n in moves:
        for _ in range(n):

            rope[0] += DIRS[d]
            current = rope[0]
            for i in range(1, N+1):
                rope[i] = update_knot(current, rope[i])
                current = rope[i]
            
            visited[rope[N]] += 1

    return visited

def update_knot(head, tail):

    if abs(head - tail) < 2:
        return tail

    d = head - tail
    x = 0 if d.real == 0 else d.real // abs(d.real)
    y = 0 if d.imag == 0 else d.imag // abs(d.imag)
    
    return tail + x + y*1j

def print_grid(rope, dimensions=((-11,14),(-5,15))):
    
    (xmin,xmax), (ymin,ymax) = dimensions

    grid = [['.'] * (xmax - xmin + 1) for _ in range(ymax - ymin + 1)]
    grid[ymax][-xmin] = 's'
    
    for i in range(len(rope)-1,-1, -1):
        knot = rope[i]
        grid[ymin-int(knot.imag)-1][int(knot.real)-xmin] = str(i) if i else 'H'

    result = ''.join([''.join(row) + '\n' for row in grid])
    print(result)

@pytest.mark.parametrize(
    ('input_data','output'),
    (
        (TEST_DATA1, EXPECTED1),
        (TEST_DATA2, EXPECTED2),
    )
)
def test_main(input_data, output):
    assert main(input_data) == output

if __name__ == "__main__":
    main(data)