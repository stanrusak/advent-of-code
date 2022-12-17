import pytest, re

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 1651, 1707

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):
    
    parse(data)

    # part 1    
    path, pressure = get_best_path(30,cutoff=100)
    part1 = pressure
    print(f"==== Part 1 ====\n\nBest path:\n\n{'->'.join(path[0])}\n")

    # part 2
    path, pressure = get_best_path_with_elephant(26,1000)
    part2 = pressure
    print(f"==== Part 2 ====\n\nBest paths:\n\nMe: {'->'.join(path[0][0])}\nElephant: {'->'.join(path[0][1])}\n")

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def parse(data):

    for line in data.splitlines():
        
        name = line[6:8]
        flow, children = line[23:].split("; ")
        children = re.split("tunnel[s]? lead[s]? to valve[s]? ", children)[-1]
        children  = children.split(", ")

        valve = Valve.get(name)
        valve.flow = int(flow)
        valve.children = [Valve.get(name) for name in children]

def get_best_path(minutes, cutoff=1000):

    flow_rate = 0
    pressure = 0
    start = [['AA'], set(), 'AA', flow_rate, pressure]
    paths = [start]
    
    for i in range(1, minutes + 1):

        print(f"Part 1: {int(100*i/minutes)}%...", end="\r")

        next_step = []
        for item in paths:

            path, on, prev, flow, pr = item
            pr += flow
            
            name = path[-1]
            current = Valve.valves[name]
            if current.flow and not (name in on):

                next_step.append([path, on | {name}, name, flow + current.flow, pr])

            for child in current.children:
                
                if child.name != prev:
                    next_step.append([path + [child.name], on, name,  flow, pr])


            next_step.sort(key=lambda x: x[-1])
            paths = next_step if len(next_step) < cutoff else next_step[-cutoff:]

    max_pressure = 0
    for path in paths:

        pr = path[-1]
        if pr > max_pressure:

            best_path = path
            max_pressure = pr

    return best_path, max_pressure

def get_best_path_with_elephant(minutes, cutoff=1000):

    flow_rate = 0
    pressure = 0
    start = [[['AA'],['AA']], set(), 'AA', flow_rate, pressure]
    paths = [start]
    
    for i in range(1,minutes + 1):

        print(f"Part 2: {int(100*i/minutes)}%...", end="\r")

        next_step = []
        for item in paths:

            [me, el], on, [prev_me, prev_el], flow, pr = item
            pr += flow
            
            name_me = me[-1]
            name_el = el[-1]
            current_me = Valve.valves[name_me]
            current_el = Valve.valves[name_el]
            
            # I turn on my current valve
            if current_me.flow and not (name_me in on):

                # elephant turns on its current valve
                if current_el.flow and not (name_el in on) and name_me != name_el:
                    next_step.append([[me, el], on | {name_me, name_el}, [name_me, name_el], flow + current_me.flow + current_el.flow, pr])

                # elephan goes straight to next valves
                for child in current_el.children:

                    if child.name != prev_el:
                        next_step.append([[me, el + [child.name]], on | {name_me}, [name_me, name_el], flow + current_me.flow, pr])

            # I went straight to the next valves 
            for child_me in current_me.children:

                if child_me.name != prev_me:

                    # elephant turns on its current valve
                    if current_el.flow and not (name_el in on):
                        next_step.append([[me + [child_me.name], el], on | {name_el}, [name_me, name_el], flow + current_el.flow, pr])
                    
                    # elephan goes straight to next valves
                    for child_el in current_el.children:

                        if child_el.name != prev_el:
                            next_step.append([[me + [child_me.name], el + [child_el.name]], on, [name_me, name_el], flow, pr])

            
        next_step.sort(key=lambda x: x[-1])
        paths = next_step if len(next_step) < cutoff else next_step[-cutoff:]

    max_pressure = 0
    for path in paths:

        pr = path[-1]
        if pr > max_pressure:
            
            best_path = path
            max_pressure = pr
    
    return best_path, max_pressure

class Valve:

    valves = {}

    def __init__(self, name):

        self.name = name

    @classmethod
    def get(cls, name):

        if name not in cls.valves:

            valve = cls(name)
            cls.valves[name] = valve
        
        else:

            valve = cls.valves[name]

        return valve

    def __repr__(self):

        return f"{self.name}: flow={self.flow}, children={[c.name for c in self.children]}"

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