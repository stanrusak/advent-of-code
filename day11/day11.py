import pytest, re

with open("input.txt", "r") as f:
    data = f.read().strip()

with open("test_input.txt", "r") as f:
    TEST_DATA = f.read().strip()
    EXPECTED = 10605, 2713310158    

def main(data):
    
    data = data.split('\n\n')
    
    part1 = compute_monkey_business(data, rounds=20, mode='direct')
    part2 = compute_monkey_business(data, rounds=10000, mode='remainder')

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def compute_monkey_business(data, rounds, mode):

    monkeys = [Monkey(info) for info in data]
    for monkey in monkeys:
        monkey.get_remainders()

    for _ in range(rounds):
        for monkey in monkeys:
            monkey.throw_all(monkeys,mode=mode)

    activity = [monkey.inspected for monkey in monkeys]
    activity.sort()

    return activity[-1] * activity[-2]

class Monkey:

    divisors = []    

    def __init__(self, info):

        self.parse(info)
        self.inspected = 0

    def parse(self, info):

        num, start, op, test, t, f = info.splitlines()
        
        p = r"\d+"
        self.num = int(re.findall(p, num)[0])
        self.items = [Item(int(n)) for n in re.findall(p, start)]
        self.divisor = int(re.findall(p, test)[0])
        self.divisors.append(self.divisor)
        self.recipient = {k:int(re.findall(p, v)[0]) for k, v in zip((True, False),(t,f))}

        op = op.split()
        self.op = op[-2]
        self.op_val = 'old' if op[-1] == 'old' else int(op[-1])

    def get_remainders(self):

        for item in self.items:
            for divisor in self.divisors:
                item.remainders[divisor] = item.val % divisor

    def throw_remainder(self, item, monkeys):
        """ Keep track only of remainders"""
        
        item.update_remainders(self.op, self.op_val)
        to = self.recipient[item.remainders[self.divisor] == 0]
        monkeys[to].catch(item)
        self.inspected += 1

    def throw_direct(self, item, monkeys):
        """ Keep track of worry level directly """ 
        
        x = item.val
        y = x if self.op_val == 'old' else self.op_val
        if self.op == '*':
            item.val = x * y
        elif self.op == '+':
            item.val = x + y

        item.val = item.val // 3

        to = self.recipient[item.val % self.divisor == 0]
        monkeys[to].catch(item)
        self.inspected += 1
    
    def catch(self, item): self.items.append(item)

    def throw_all(self, monkeys, mode):

        while self.items:

            item = self.items.pop(0)

            if mode == 'direct':
                self.throw_direct(item,monkeys)
            elif mode == 'remainder':
                self.throw_remainder(item,monkeys)

class Item:

    def __init__(self,val):

        self.val = val
        self.remainders = {}
    
    def update_remainders(self, op, val):

        for divisor, remainder in self.remainders.items():

            if op == '*':

                if val == 'old':
                    self.remainders[divisor] = (remainder ** 2) % divisor
                else:
                    self.remainders[divisor] = (remainder * val) % divisor
                
            elif op == '+':

                self.remainders[divisor] = (remainder + val) % divisor

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