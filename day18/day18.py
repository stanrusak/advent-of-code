import pytest

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    # part 1
    cubes, bounds = parse(data)
    area = get_surface_area(cubes, bounds)
    part1 = area

    # part 2
    airpockets = get_airpockets(cubes, bounds)
    for airpocket in airpockets:

        area -= get_surface_area(airpocket, bounds)
    
    part2 = area

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_airpockets(cubes, bounds):

    airpockets = []
    for x in range(*bounds[0]):
        for y in range(*bounds[1]):
            for z in range(*bounds[2]):
                
                seen = False
                for airpocket in airpockets:
                    if (x, y, z) in airpocket:
                        seen = True
                        break

                if (x,y,z) not in cubes and not seen:
                    
                    airpocket = explore_airpocket((x,y,z), cubes, bounds)
                    if airpocket:
                        airpockets.append(airpocket)

    return airpockets

def get_surface_area(cubes, bounds):

    area = 0
    for x, y, z in cubes:

        sides = 6
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:

            if (x+dx, y+dy, z+dz) in cubes:
                sides -= 1
        
        area += sides
    
    return area
    
def explore_airpocket(coords, cubes, bounds):

    airpocket = {coords}
    frontier = [coords]
    seen = set()

    while frontier:

        x, y, z = frontier.pop()

        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:

            xx, yy, zz = x + dx, y + dy, z + dz
            if xx == bounds[0][0] - 1 or xx == bounds[0][1] + 1 or yy == bounds[1][0]  - 1 or yy == bounds[1][1] + 1 or zz == bounds[2][0] - 1 or zz == bounds[2][1] + 1:
                return None

            if (xx, yy, zz) not in cubes and (xx, yy, zz) not in seen:

                airpocket.add((xx, yy, zz))
                seen.add((xx, yy, zz))
                frontier.append((xx, yy, zz))

    return airpocket
            
def parse(data):

    coords = set()
    xmax = ymax = zmax = 0
    xmin = ymin = zmin = 100
    for line in data.splitlines():

        x, y, z = list(map(int, line.split(',')))
        coords.add((x, y, z))
        xmax = max(x, xmax)
        ymax = max(y, ymax)
        zmax = max(z, zmax)
        xmin = min(x, xmin)
        ymin = min(y, ymin)
        zmin = min(z, zmin)

    return coords, ((xmin, xmax + 1),(ymin, ymax + 1), (zmin, zmax + 1))

TEST_DATA = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
EXPECTED = 64, 58

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