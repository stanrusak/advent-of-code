import pytest

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

    root = parse_input(data)
    print(root)
    
    part1 = get_cumulative_size(root, 100000)

    capacity = 70_000_000
    free = capacity - root.size
    needed = 30_000_000 - free

    dirs = list_dirs(root)
    dirs.sort(key=lambda x: x.size)
    
    for d in dirs:
        if d.size > needed:
            part2 = d.size
            break

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def parse_input(data):

    commands = data.split('$ cd ')[1:]
    filesystem = Dir('filesystem')
    current = filesystem
    for command in commands:

        if command[:2] == "..":
            current = current.parent

        else:

            name, ls_output = command.split('\n$ ls\n')

            if name not in current.dirs:
                d = Dir(name, parent=current)
                d.get_files(ls_output)
                current.dirs.append(d)
            current = d

    return filesystem.dirs[0]            

def get_cumulative_size(root, threshold):

    size = 0
    if root.size < threshold:
        size += root.size

    for d in root.dirs:
        size += get_cumulative_size(d, threshold=threshold)

    return size

def list_dirs(root):

    dirs_list = []
    for d in root.dirs:
        dirs_list += list_dirs(d)
    dirs_list.append(root)
        
    return dirs_list

class Dir:

    def __init__(self, name, parent=None):
        
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = []
        self._size = None
    
    def get_files(self, ls_output):

        for line in ls_output.splitlines():
              
            if line[0] in "123456789":
                size, name = line.split()
                self.files.append(File(name, size))

    @property
    def size(self):

        if self._size:
            return self._size
        else:
            return self.get_size()

    def get_size(self):

        size = 0
        for d in self.dirs:
            size += d.get_size()
        
        for f in self.files:
            size += f.size

        self._size = size

        return size

    def tree(self, level=0):

        result = ""
        for d in self.dirs:
            result += "  "*level +  "📁 " + d.name + '\n'
            result += d.tree(level + 1)
        for d in self.files:
             result += "  "*level + "🗎 " + d.name + '\n'
        return result

    def __repr__(self):

        return self.tree()

class File:

    def __init__(self, name, size):

        self.name = name
        self.size = int(size)


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