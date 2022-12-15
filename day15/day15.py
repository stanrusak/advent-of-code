import pytest, re
from collections import deque

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    Y, YMAX = 10, 20
    EXPECTED = 26, 56000011

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data, yval=2000000, ymax=4000000):
    
    sensors = [list(map(int, re.findall(r"-?\d+", line))) for line in data.splitlines()]
    sensors.sort(key=lambda x: x[0])

    # part 1
    xmin, xmax = excluded(sensors, yval).pop()
    part1 = xmax - xmin

    # part 2
    for y in range(ymax):
        
        if y % 40000 == 0:
            print(f"Scanning {y//40000}%...", end="\r")
        
        ranges = excluded(sensors, y)

        if len(ranges) > 1:
            x = ranges[0][1] + 1
            print(f"Found the distress beacon at {x, y}!")
            break

    part2 = y + 4000000 * x

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def excluded(sensors, y):

    ranges = deque()
    for sensor in sensors:

        r = scanned_range(sensor, y)
        if r:
            ranges.append(r)
    
    ranges = consolidate(ranges)
    
    return ranges

def scanned_range(sensor, y):

    xs, ys, xb, yb = sensor
    manhattan_distance = abs(xs - xb) + abs(ys - yb)
    dx = manhattan_distance - abs(ys - y)

    if dx >= 0:
        return [xs - dx, xs + dx]

def consolidate(ranges):

    length = len(ranges)
    current = ranges.popleft()
    consolidated = []
    while ranges:

        next_ = ranges.popleft()
        if current[1] >= next_[0] - 1:
            current[0] = min(current[0], next_[0])
            current[1] = max(current[1], next_[1])
        else:
            consolidated.append(current)
            current = next_
    
    consolidated.append(current)
    ranges = deque(consolidated)

    if len(ranges) != length:
        return consolidate(ranges)        

    return ranges 

@pytest.mark.parametrize(
    ('input_data','yval','ymax','output'),
    (
        (TEST_DATA, Y, YMAX, EXPECTED),
    )
)
def test_main(input_data, yval, ymax, output):
    assert main(input_data, yval, ymax) == output

if __name__ == "__main__":
    main(data)