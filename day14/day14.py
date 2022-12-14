import pytest

TEST_DATA = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 24, 93

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    grid = parse(data)

    start = 500, 0
    part1 = count_grains(start, grid)
    grid.show("Part 1")

    parse(data)
    grid.add_floor()
    part2 = count_grains(start, grid)
    grid.show("Part 2")

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def count_grains(start, grid):

    grains = 0
    while True:

        try:
            move_grain(start, grid)
            grains += 1
            if grid(*start) == 'o':
                return grains
        except AaaahFallingIntoTheAbyssError:
            return grains

def move_grain(start, grid):

    x, y = start

    if (x <= 0 or x >= len(grid[0])-1 or y >= len(grid) - 1):
        raise AaaahFallingIntoTheAbyssError("AAAAAAAAAHHH!!!")

    if grid.empty(x,y+1):
        move_grain((x, y+1), grid)

    else:

        if grid.empty(x-1, y+1):
            move_grain((x-1, y+1), grid)
        elif grid.empty(x+1, y+1):
            move_grain((x+1, y+1), grid)
        else:
            grid[y][x] = 'o'

def parse(data):

    coords = []
    maxy = 0
    for line in data.splitlines():

        rockline = []
        for c in line.split(' -> '):

            x, y = list(map(int, c.split(',')))
            rockline.append((x, y))
            maxy = max(maxy, y)

        coords.append(rockline)

    grid = Grid((1000, maxy))
    grid.fill(coords)

    return grid

class Grid(list):

    def __init__(self, dims, fill='.'):

        self._fill = fill
        super().__init__([[fill for _ in range(dims[0]+1)] for _ in range(dims[1]+1)])

    def show(self, title, crop=75):

        l = (2 * crop - len(title)) // 2 
        r = "\n" + "=" * (l - 1) + f" {title} " + "=" * (l - 1) + "\n"
        r += '\n'.join(''.join(line[500-crop:500+crop]) for line in self)
        print(r)
    
    def __call__(self, x, y): return self[y][x]

    def empty(self, x, y): return self[y][x] == self._fill

    def fill(self, coords):

        for line in coords:
            
            current = line.pop(0)
            while line:

                next_ = line.pop(0)
                
                if current[0] == next_[0]:
                    
                    for y in range(min(current[1],next_[1]), max(current[1],next_[1]) + 1):
                        self[y][current[0]] = '#'
                
                elif current[1] == next_[1]:
                    
                    for x in range(min(current[0], next_[0]), max(current[0], next_[0]) + 1):
                        self[current[1]][x] = '#'

                current = next_

    def add_floor(self):

        self.append(['.']*len(self[0]))
        self.append(['#']*len(self[0]))

class AaaahFallingIntoTheAbyssError(Exception):
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