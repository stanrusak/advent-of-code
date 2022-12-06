import pytest

TEST_DATA = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    ]
EXPECTED = [(7, 19), (5, 23), (6, 23), (10, 29), (11, 26)]

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    part1 = find_marker(data, 4)
    print(f"Part 1: {part1}")
    
    part2 = find_marker(data, 14)
    print(f"Part 2: {part2}")
    
    return part1, part2
    
def find_marker(data, marker_length):

    for i in range(marker_length - 1 , len(data)):
        if len(set(data[i-marker_length + 1:i+1])) == len(data[i-marker_length + 1:i+1]):
            return i + 1

@pytest.mark.parametrize(
    ('input_data','output'),
    tuple(zip(TEST_DATA, EXPECTED))
)
def test_main(input_data, output):
    assert main(input_data) == output

if __name__ == "__main__":
    main(data)