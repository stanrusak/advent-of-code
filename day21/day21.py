from copy import deepcopy
import pytest

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 152, 301

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    # part 1
    monks = get_tree(data)
    compute(monks)
    part1 = int(monks['root'].val)

    # part 2
    monks = get_tree(data, human=True)
    part2 = int(get_human_humber(monks))

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def get_human_humber(monks):

    monks1 = deepcopy(monks)
    monks2 = deepcopy(monks)

    monks1['humn'].val = 0
    compute(monks1)

    monks2['humn'].val = 1
    compute(monks2)

    if monks1['root'].child1.val == monks2['root'].child1.val:
        
        monkey_branch = monks1['root'].child1.name
        human_branch = monks1['root'].child2.name

    else:

        monkey_branch = monks1['root'].child2.name
        human_branch = monks1['root'].child1.name

    target = monks1[monkey_branch].val
    
    return binary_search(monks, human_branch, target)

def binary_search(monks, human_branch, target):

    # determine upper bound
    min_distance = float('inf')
    upper = 1
    while True:

        distance = abs(human_branch_val(monks, human_branch, upper) - target)
        if distance > min_distance:
            break
        
        min_distance = distance
        upper *= 10

    # binary search among possible human numbers
    lower = 0
    upper = distance
    while upper > lower:

        distance_low = abs(human_branch_val(monks, human_branch, lower) - target)
        distance_high = abs(human_branch_val(monks, human_branch, upper) - target)

        if distance_low >= distance_high:
            lower = (upper + lower) // 2
        elif distance_low < distance_high:
            upper = (lower + upper) // 2

    return lower

def human_branch_val(monks, human_branch, number):

    m = deepcopy(monks)
    m['humn'].val = number
    compute(m)
    return m[human_branch].val

def compute(monks):

    while monks['root'].val is None:
        for monk in monks.values():
            monk.calc()

def get_tree(data, human=False):

    monks = {}

    for line in data.splitlines():

        parent_name, rest = line.split(": ")

        try:
            rest = int(rest)
        
        except ValueError:
            pass

        if parent_name not in monks:

            monks[parent_name] = Node(parent_name)
            
        parent = monks[parent_name]

        if isinstance(rest, int):

            parent.val =  rest

            if human and parent_name == 'humn':
                parent.val = None

            if parent.parent:
                parent.parent.calc()
        
        else:

            monk1, op, monk2 = rest.split()
            parent.op = op
            
            if monk1 not in monks:
                monks[monk1] = Node(monk1, parent=parent)
            
            if monk2 not in monks:
               monks[monk2] = Node(monk2, parent=parent)
            
            parent.child1 = monks[monk1]
            parent.child2 = monks[monk2]
            parent.calc()

    return monks

class Node:

    def __init__(self, name, parent=None, child1=None, child2=None, op=None, val=None):

        self.name = name
        self.parent = parent
        self.child1 = child1
        self.child2 = child2
        self.op = op
        self.val = val

    def calc(self):

        if not self.child1 or self.child1.val is None:
            return

        if not self.child2 or self.child2.val is None:
            return
        
        self.val = op(self.child1.val, self.child2.val, self.op)
        
        if self.parent:
            self.parent.calc()
        
    def __repr__(self): return f"{self.name} (val: {self.val}, child1={self.child1} child2={self.child2})"

def op(num1, num2, op):

    if op == '+':
        return num1 + num2
    if op == '-':
        return num1 - num2
    if op == '*':
        return num1 * num2
    if op == '/':
        return num1 / num2

    raise AssertionError("unreachable")

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