import pytest

with open("test.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 13140, None


with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    # data = TEST_DATA
    instructions = [line for line in data.splitlines()]

    cpu = CPU()
    for instruction in instructions:
        cpu.execute(instruction)
    
    current = 0
    screen = ''
    for i, X in enumerate(cpu.history):

        screen += '#' if abs(X - (current % 40)) < 2 else '.'
        if (i + 1) % 40 == 0:
            screen += '\n'

        current += 1
        # print(f"cycle: {i+1}, X: {X}")
    print(screen)
    

    part1 = sum(cpu.scores)
    part2 = None

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

class CPU:

    def __init__(self):

        self.clock = 1
        self.X = 1
        self.scores = []
        self.history = [1]

    def tick(self):

        # print(f"clock: {self.clock}, X: {self.X}, scores: {self.scores}")
        self.clock += 1
        self.history.append(self.X)
        
        if (self.clock - 20) % 40 == 0:
            self.scores.append(self.X * self.clock)

    def add(self, val): self.X += val

    def execute(self, instruction):

        if instruction.startswith("noop"):
            self.tick()
            return
        
        if instruction.startswith("addx"):
            val = int(instruction[5:])
            self.tick()
            self.add(val)
            self.tick()

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