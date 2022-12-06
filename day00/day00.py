import pytest

TEST_DATA = """\

"""
EXPECTED = 0, None

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):
    
    part1 = 0
    part2 = None

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

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