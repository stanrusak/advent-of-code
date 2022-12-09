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
    visited = tug_on_rope(moves,knots)
    part1 = len(visited.values())
    
    knots = 9
    visited = tug_on_rope(moves, knots) 
    part2 = len(visited.values())

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def tug_on_rope(moves, N):

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

        # print(f"== {d} {n} ==\n")
        # print_grid(rope)

    return visited

def update_knot(head, tail):

    for x in [-1,0,1]:
        for y in [-1j, 0j, 1j]:
            if head == tail + x + y:
                return tail

    for radius in range(2,10):

        for x in range(-radius, radius + 1):
            for y in [-radius, radius]:
                if head == tail + x + y*1j:
                    
                    ystep = (y // abs(y))
                    if abs(x) < 2:
                        return head - ystep*1j
                    
                    else:
                        return head - ystep*1j - x // abs(x)

        for y in range(-radius+1, radius):
            for x in [-radius, radius]:
                if head == tail + x + y*1j:
                    
                    xstep = (x // abs(x))
                    if abs(y) < 2:
                        return head - xstep
                    
                    else:
                        return head - xstep - (y // abs(y))*1j

    raise NotImplementedError(f"Weird case: head={head}, tail={tail}, x={x}, y={y}")

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