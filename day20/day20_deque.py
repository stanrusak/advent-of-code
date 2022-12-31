from collections import deque
import pytest

DECRYPTION_KEY = 811589153

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    # part 1
    numbers = [int(number) for number in data.splitlines()]
    decoder = Decoder(numbers)
    for i, n in enumerate(numbers):
        decoder.shift(i, n)
    
    # part 2
    numbers = [num * DECRYPTION_KEY for num in numbers]
    decoder2 = Decoder(numbers)
    for _ in range(10):
        for i, n in enumerate(numbers):
            decoder2.shift(i, n)
    
    part1 = decoder.coordinates()
    part2 = decoder2.coordinates()

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

class Decoder(deque):

    def __init__(self, lst):

        super().__init__()
        for i, n in enumerate(lst):
            self.append((i, n))
            if n == 0:
                self.zero = (i, n)
        self.key = 1

    def shift(self, i, num):

        idx = self.index((i, num))
        self.rotate(-idx)
        self.popleft() 

        rotation = num % len(self)
        self.rotate(-rotation)
        self.appendleft((i, num))

    def coordinates(self):

        i = self.index(self.zero)
        return sum([self[(i + num) % len(self)][1] for num in [1000,2000,3000]])
    
    def to_list(self): return [x[1] for x in self]

    def __repr__(self, start=1): return str(self.to_list)
    
TEST_DATA = """\
1
2
-3
3
-2
0
4
"""
EXPECTED = 3, 1623178306

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