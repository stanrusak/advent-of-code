import pytest

TEST_DATA = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
EXPECTED = 3068, 1514285714288

SHAPES = [
    ["####"],
    [".#.","###",".#."],
    ["..#","..#","###"],
    ["#","#","#","#"],
    ["##","##"]
]

WIDTH = 7
MATCH_LENGTH = 10

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    part1 = get_height(data, rocks=2022)
    part2 = get_height(data, rocks=1000000000000)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_height(jets, rocks):

    filled = set((i, 0) for i in range(WIDTH))
    highest = 0

    jet_idx = 0
    indices = [(0, 0)]
    heights = [0]
    repeating = False
    for i in range(rocks):
        
        shape_idx = i % len(SHAPES)
        jet_idx, highest = drop_shape(jets, jet_idx, shape_idx, filled, highest)
        
        if len(indices) > MATCH_LENGTH and match(indices):
            repeating = True
            break
        
        indices.append((shape_idx, jet_idx % len(jets)))
        heights.append(highest)

    if not repeating:
        return highest

    start = indices.index(indices[-MATCH_LENGTH])
    repeat = len(indices) - MATCH_LENGTH - start
    height_diff = heights[-MATCH_LENGTH] - heights[start]

    rocks = rocks - start
    rep, rem = divmod(rocks, repeat)
    
    return heights[start + rem] + rep * height_diff

def match(indices):

    for i in range(0, len(indices) - MATCH_LENGTH):

        if indices[i] == indices[-MATCH_LENGTH]:
            
            cand = True
            for j in range(1, MATCH_LENGTH):

                if indices[i + j] != indices[-MATCH_LENGTH + j]:
                    cand = False
                    break
            
            if cand:
                return True

    return False

def drop_shape(jets, jet_idx, shape_idx, filled, highest):

    x, y = 2, highest + 4
    shape = SHAPES[shape_idx]
    add_walls(filled, highest)

    while True:

        jet = jets[jet_idx % len(jets)]

        if jet == '>':
            
            clear = True
            for j, row in enumerate(shape):
                
                i = len(row)
                if row[-1] == "#":
                    if (x + i,  y + len(shape) - 1 - j) in filled:
                        clear = False
                        break
                elif row[1] == "#" and (x + 2,  y + len(shape) - 1 - j) in filled:
                    clear = False
                    break
            
            if clear:
                x += 1

        elif jet == '<':
        
            clear = True
            for j, row in enumerate(shape):
                
                if row[0] == "#":
                    if (x - 1,  y + len(shape) - 1 - j) in filled:
                        clear = False
                        break
                elif row[1] == "#" and (x,  y + len(shape) - 1 - j) in filled:
                    clear = False
                    break
            
            if clear:
                x -= 1

        else:
            raise AssertionError('unreachable')

        jet_idx += 1

        clear = True
        for i, c in enumerate(shape[-1]):

            if c == '#' and (x + i, y - 1) in filled:
                clear = False
                break
        
        if shape_idx % len(shape) == 1:

            for i, c in enumerate(shape[-2]):

                if c == '#' and (x + i, y) in filled:

                    clear = False
                    break
            
        if clear:
            y -= 1
        
        else:
            
            for j, row in enumerate(shape):
                for i, c in enumerate(row):
                    
                    if c == '#':
                        yy = y + len(shape) -  1 - j
                        filled.add((x + i, yy))
                        highest = max(highest, yy)
            
            return jet_idx % len(jets), highest

def add_walls(filled, highest):

    for y in range(highest + 1, highest + 7):
        
        filled.add((-1,y))
        filled.add((WIDTH,y))

def pr(filled, highest):

    for j in range(highest + 4, -1, -1):

        row = f'{j:>2}'
        for i in range(-1, WIDTH + 1):
            
            if (i, j) == (-1, 0) or (i, j) == (WIDTH, 0):
                row += '+'
            
            elif j == 0:
                row += '-'
            
            elif i == -1 or i == WIDTH:
                row += '|'
            
            elif (i, j) in filled:
                row += '#'
            
            else:
                row += '.'
        
        print(row)
    
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