from math import ceil
import re, pytest

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 33, 62 * 56

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):
    
    blueprints = parse(data)

    # part 1 
    quality = 0
    for i, blueprint in enumerate(blueprints, start=1):

        paths = get_paths_optimized(blueprint, 24)
        best = max(paths, key=lambda x: x[-1][-1])
        geodes = best[-1][-1]
        quality += i * geodes
        print(f"Part 1: {100 * i // len(blueprints)}%...", end="\r")
    
    # part 2
    max_geodes = 1
    blueprints = blueprints[:3]
    for i, blueprint in enumerate(blueprints, start=1):

        paths = get_paths_optimized(blueprint, 32)
        best = max(paths, key=lambda x: x[-1][-1])
        geodes = best[-1][-1]
        max_geodes *= geodes
        print(f"Part 2: {100 * i // len(blueprints)}%...   ", end="\r")

    part1 = quality
    part2 = max_geodes

    print(f"Part 1: {part1}   ")
    print(f"Part 2: {part2}   ")

    return part1, part2

def get_paths_optimized(blueprint, minutes, cutoff=24, buffer=10000):

    if minutes <= cutoff:
        return get_paths(blueprint, minutes)

    paths = get_paths(blueprint, cutoff)
    
    for _ in range(1, minutes - cutoff + 1):

        if len(paths) > buffer:
            paths = sorted(paths, key=lambda path: (path[-1][-1], path[-1][-2]))[-buffer:]

        paths = [path + (1, ) for path in paths]
        paths = get_paths(blueprint, 1, paths)

    return paths 

def get_paths(blueprint, minutes, paths=None):

    build = []

    robots = [1,0,0,0]
    resources = [0,0,0,0]
    costs = [blueprint[res] for res in ["ore", "clay", "obsidian", "geode"]]

    if not paths:
        paths = [(build, robots, resources, minutes)]
    finished = []
    while paths:
    
        build, robots, resources, remaining = paths.pop()

        for robot in range(4):

            max_cost = 0
            for resource in range(3):

                if costs[robot][resource] and not robots[resource]:
                    max_cost = 0
                    break

                if not costs[robot][resource] or not robots[resource]:
                    continue
                
                cost = ceil((costs[robot][resource] - resources[resource]) / robots[resource]) + 1
                max_cost = max(max_cost, cost)

            if max_cost < 1:
                continue
            
            if remaining < max_cost:
                
                new_resources = [resource_count + remaining * robots[resource] for resource, resource_count in enumerate(resources)]
                path = (build, robots, new_resources)
                if not finished or path != finished[-1]:
                    finished.append(path)
                continue
            
            new_resources = [resource_count + max_cost * robots[resource] for resource, resource_count in enumerate(resources)]
            
            for resource in range(3):

                new_resources[resource] -= costs[robot][resource]

            new_robots = robots.copy()
            new_robots[robot] += 1
            paths.append((build + [robot], new_robots, new_resources, remaining - max_cost))        
    
    return finished
                
def parse(data):

    blueprints = []
    for line in data.splitlines():

        robots = {}
        _, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = list(map(int, re.findall(r'\d+', line)))
        robots['ore'] = (ore_ore, 0, 0)
        robots['clay'] = (clay_ore, 0, 0)
        robots['obsidian'] = (obsidian_ore, obsidian_clay, 0)
        robots['geode'] = (geode_ore, 0, geode_obsidian)
        blueprints.append(robots)
    
    return blueprints

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