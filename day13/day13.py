import pytest
from itertools import zip_longest
from functools import cmp_to_key
from sys import argv

PRINT = False
if len(argv) == 2 and argv[1] == '-v':
    PRINT = True

with open("input.txt", "r") as f:
    data = f.read().strip()

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 13, 140

def main(data):

    global PRINT
    packets = [[eval(line) for line in p.splitlines()] for p in data.split("\n\n")]
    
    pr("=== Part 1 ===\n\n")
    part1 = 0
    for i, packet in enumerate(packets, start=1):
        
        pr(f"\n== Pair {i} ==")
        left, right = packet
        c = compare(left, right)
        if c == 1:
            part1 += i

    PRINT = False
    packets = [eval(line) for line in data.splitlines() if line]
    packets.extend([[[2]], [[6]]])
    packets.sort(key=cmp_to_key(compare), reverse=True)
    
    part2 = 1
    for i, packet in enumerate(packets, start=1):
        if packet == [[2]] or packet == [[6]]:
            part2 *= i

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def compare(left, right, nesting=0):

    pr(f"- Compare {left} vs {right}", nesting)
    nesting += 2

    if isinstance(left, int) and isinstance(right, int):

        if left < right:
            pr(f"- Left side is smaller, so inputs are in the right order", nesting)
            return 1
        elif left == right:
            return 0
        elif left > right:
            pr(f"- Right side is smaller, so inputs are not in the right order", nesting)
            return -1

    if isinstance(left, int) and isinstance(right, list):
        pr(f"- Mixed types; convert left to {[left]} and retry comparison", nesting)
        left = [left]
    
    if isinstance(left, list) and isinstance(right, int):
        pr(f"- Mixed types; convert right to {[right]} and retry comparison", nesting)
        right = [right]

    for l, r in zip_longest(left, right):
        
        if l is None:
            pr("- Left side ran out of items, so inputs are in the right order", nesting)
            return 1
        if r is None:
            pr("- Right side ran out of items, so inputs are not in the right order", nesting)
            return -1

        comparison = compare(l, r, nesting)
        if comparison:
            return comparison
    
    return 0

def pr(message, nesting=0):
    if PRINT:
        print(f"{' '*nesting}{message}")

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