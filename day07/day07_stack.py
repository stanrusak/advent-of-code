import pytest
from collections import defaultdict

TEST_DATA = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 95437, 24933642

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    sizes = get_sizes(data)

    part1 = sum([val for val in sizes.values() if val < 100000])

    total = 70000000
    free = total - sizes['/']
    needed = 30000000 - free
    
    for size in sorted([val for val in sizes.values()]):
        if size >= needed:
            part2 = size
            break 
    
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_sizes(data):

    commands = data.split('$ cd ')[1:]

    stack = []
    sizes = defaultdict(int)
    
    for command in commands:

        if command.startswith('..'):

            stack.pop()
            sizes['/'.join(stack)] += size
            size = sizes['/'.join(stack)]
        
        else:

            name, ls_out = command.split('\n$ ls\n')
            stack.append(name)
            size = get_size(ls_out)
            sizes['/'.join(stack)] += size

    while len(stack) > 1:

        stack.pop()
        sizes['/'.join(stack)] += size
        size = sizes['/'.join(stack)]

    return sizes

def get_size(ls_out):

    total = 0
    for line in ls_out.splitlines():
        
        if line[0].isnumeric():

            size, _ = line.split()
            total += int(size)

    return total

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