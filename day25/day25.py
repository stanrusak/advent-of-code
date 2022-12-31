import pytest
from math import log

DIGITS = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
CUTOFF = 100

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    total = 0
    for s in data.splitlines():
        total += SNAFU_to_decimal(s)

    snafu = decimal_to_SNAFU(total)
    assert total == SNAFU_to_decimal(snafu)

    part1 = snafu
    print(f"Answer: {snafu}")

    return part1
    
def SNAFU_to_decimal(snafu):

    number = 0
    for i, d in enumerate(snafu[::-1]):

        number += DIGITS[d] * 5 ** i
    
    return number

def decimal_to_SNAFU(decimal):

    exp = int(log(decimal, 5))

    frontier = [('', decimal)]
    while exp > -1:

        new_frontier = []
        for snafu, remainder in frontier:

            if not remainder:
                return snafu + '0'*(exp + 1)

            for char, val in DIGITS.items():

                new_frontier.append((snafu + char, remainder - val * 5**exp))
        
        frontier = new_frontier
        frontier = sorted(frontier, key=lambda x: abs(x[1]))[:CUTOFF]
        exp -= 1

    return new_frontier

TEST_DATA = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
EXPECTED = '2=-1=0'

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