import pytest

with open("input.txt", "r") as f:
    data = f.read().strip()

ADJACENT = [0, 1, -1, 1j, -1j]

def main(data):
    
    start, end, walls, blizzards = parse(data)
    walls = walls | {-1j, -1j+1, -1j+2} | {end + 1j, end - 1 + 1j, end + 1 + 1j} # wall in entrance and exit prevent exploring outside the map
    
    print("\nGoing there...")
    minute, paths = bfs(start, end, walls, blizzards)
    part1 = minute
    
    print("\n...and back again...                 ")
    minute, paths = bfs(end, start, walls, blizzards, minute, paths)

    print("\n...and there again...                ")
    minute, paths = bfs(start, end, walls, blizzards, minute, paths)
    part2 = minute

    print()
    print(f"Part 1: {part1}                     ")
    print(f"Part 2: {part2}                     ")

    return part1, part2

def bfs(start, end, walls, blizzards, minute=0, paths=None):

    width = int(abs(end.real - start.real)) + 1
    height = int(abs(end.imag - start.imag)) - 1

    finished = []
    minute += 1
    frontier = [[start]] if not paths else paths
    while True:
        
        new_frontier = []

        seen = set()
        for path in frontier:

            for d in ADJACENT:
                
                new = path[-1] + d
                
                if new == end:
                    path.append(new)
                    finished.append(path)
                    
                if new in walls or new in seen:
                    continue

                mw = minute % width
                mh = minute % height
                if free(new, mw, mh, width, height, blizzards):
                    
                    seen.add(new)
                    new_path = path + [new]
                    new_frontier.append(new_path)
        
        frontier = new_frontier

        print(f"Minute {minute}: {min(abs(end-path[-1]) for path in frontier): .2f} from goal...", end="\r")
        if finished: 
            print(f"Reached in {minute} minutes.          ")
            return minute, finished
        
        minute += 1

    raise AssertionError("No Path Found!")

def left_moving(point, mw, mh, width, height, blizzards):

    if point + mw in blizzards['<']: return True
    if 1j*point.imag + (point.real + mw) % width in blizzards['<']: return True
    return False

def up_moving(point, mw, mh, width, height, blizzards):

    if point + 1j*mh in blizzards['^']: return True
    if point.real + 1j*((point.imag + mh) % height) in blizzards['^']: return True
    return False

def right_moving(point, mw, mh, width, height, blizzards):

    if point - mw in blizzards['>']: return True
    if 1j*point.imag + width - ((width - point.real + mw) % width) in blizzards['>']: return True
    return False

def down_moving(point, mw, mh, width, height, blizzards):

    if point - 1j*mh in blizzards['v']: return True
    if point.real + 1j*(height - ((height - point.imag + mh) % height)) in blizzards['v']: return True
    return False

def free(point, mw, mh, width, height, blizzards):

    return False if any(blizzard(point, mw, mh, width, height, blizzards) for blizzard in [left_moving, right_moving, up_moving, down_moving]) else True

def parse(data):

    walls, empty = set(), set()
    blizzards = {'<': set(), '>': set(), '^': set(), 'v': set()}
    for r, row in enumerate(data.splitlines()):
        for c, char in enumerate(row):

            if char == '#':
                walls.add(1j*r + c)

            elif char == '.':
                empty.add(1j*r + c)

            else:
                blizzards[char].add(1j*r + c)

    start = min(empty, key=lambda x: x.imag)
    end = max(empty, key=lambda x: x.imag)
    
    return start, end, walls, blizzards

def show(minute, start, end, walls, blizzards):

    width = int(end.real - start.real + 1)
    height = int(end.imag - start.imag - 1)
    mw = minute % width
    mh = minute % height

    grid = ''
    for r in range(0, int(end.imag) + 1):
        for c in range(0, int(end.real) + 2):

            p = c + 1j * r
            if p in walls:
                grid += '#'
            
            else:
                
                count = 0
                if left_moving(p, mw, mh, width, height, blizzards):
                    char = '<'
                    count += 1

                if up_moving(p, mw, mh, width, height, blizzards):
                    char = '^'
                    count += 1

                if right_moving(p, mw, mh, width, height, blizzards):
                    char = '>'
                    count += 1

                if down_moving(p, mw, mh, width, height, blizzards):
                    char = 'v'
                    count += 1
                
                if not count: char = '.'
                elif count > 1: char = str(count)
                grid += char

        grid += '\n'
    
    print(f"Minute {minute}")
    print(grid)
    print('\n')
    
TEST_DATA = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
EXPECTED = 18, 54

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