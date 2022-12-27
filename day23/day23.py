import pytest
from collections import defaultdict

with open("input.txt", "r") as f:
    data = f.read().strip()

ROUNDS = 1000
SEARCH = [
    [[-1j, -1j + 1, -1j - 1], -1j],
    [[1j, 1j + 1, 1j - 1], 1j],
    [[-1, 1j - 1, -1j - 1], -1],
    [[1, -1j + 1, 1j + 1], 1],
]
ADJACENT = [1, -1, 1j, -1j, 1 + 1j, 1-1j, -1+1j, -1-1j]

def main(data):
    
    search_id = 0
    elves = parse(data)

    for rounds in range(1, ROUNDS):

        # progress
        if 100 * rounds % ROUNDS == 0:
            print(f"{100 * rounds // ROUNDS}%...", end="\r")

        stopped = 0
        proposed = defaultdict(int)
        for position in elves:

            # check for stopped elves
            if all(position + d not in elves for d in ADJACENT):
                stopped += 1
                continue
            
            # check for free directions
            free = False
            for i in range(4):
                
                search, move = SEARCH[(search_id + i) % 4]
                if all(position + d not in elves for d in search):
                    free = True
                    break

            # propose new position if available    
            propose = position + move if free else position
            proposed[propose] += 1
            elves[position] = propose
        
        # check for multiply proposed positions
        new_elves = {}
        for position, proposition in elves.items():

            if proposed[proposition] < 2:
                new_elves[proposition] = proposition

            else:
                new_elves[position] = position
        
        # rotate searching strategies and reset elves
        search_id = (search_id + 1) % 4
        elves = new_elves

        # report part1 after 10 rounds
        if rounds == 10:
            part1 = get_rectangle(elves)

        # break if no elves move
        if len(elves) == stopped:
            break
                        
    part2 = rounds

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_rectangle(elves):

    minr = minc = float('inf')
    maxr = maxc = -float('inf')
    for p in elves:

        minc = min(minc, p.real)
        maxc = max(maxc, p.real)
        minr = min(minr, p.imag)
        maxr = max(maxr, p.imag)

    return int((maxr - minr + 1) * (maxc - minc + 1) - len(elves))

def parse(data):

    elves = {}
    
    for r, row in enumerate(data.splitlines()):
        for c, char in enumerate(row):

            if char == '#':
                elves[1j * r + c] = 1j * r + c
            
    return elves

def show(elves):

    rows = []
    for r in range(-2, 10):

        row = ''
        for c in range(-3, 11):

            row += '#' if (1j * r + c) in elves else '.'
    
        rows.append(row)
    
    print('\n'.join(rows))

TEST_DATA = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
EXPECTED = 110, 20
    
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