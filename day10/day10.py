import pytest

with open("input.txt", "r") as f:
    data = f.read().strip()

with open("test.txt", "r") as f:
    TEST_DATA = f.read().strip()

with open("expected.txt", "r") as f:
    expexted_screen = f.read()

EXPECTED = 13140, expexted_screen

def main(data):

    instructions = [line for line in data.splitlines()]

    device = Device()
    for instruction in instructions:
        device.execute(instruction)

    part1 = sum(device.scores)
    part2 = device.screen

    print(f"Part 1: {part1}")
    print(f"Part 2:\n\n{part2}")

    return part1, part2

class Device:

    def __init__(self):

        self.clock = 1
        self.X = 1
        self.scores = []
        self.screen = ''
        self.pixel = 0

        self.draw()

    def tick(self):

        self.clock += 1
        self.draw()

        if (self.clock - 20) % 40 == 0:
            self.scores.append(self.X * self.clock)


    def execute(self, instruction):

        if instruction.startswith("noop"):
            
            self.tick()
            return
        
        if instruction.startswith("addx"):
            
            val = int(instruction[5:])
            self.tick()
            self.add(val)
            self.tick()

    def add(self, val): self.X += val
    
    def draw(self):

        if self.pixel > 239:
            return

        self.screen += '#' if abs(self.X - (self.pixel % 40)) < 2 else '.'
        if self.clock % 40 == 0:
            self.screen += '\n'
        
        self.pixel += 1

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