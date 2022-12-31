from collections import deque
import pytest

DECRYPTION_KEY = 811589153

with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    # part 1
    numbers = [int(number) for number in data.splitlines()]
    decoder = LinkedList(numbers)
    
    for i, n in enumerate(numbers):
        decoder.shift(i, n)

    # part 2
    numbers = [num * DECRYPTION_KEY for num in numbers]
    decoder2 = LinkedList(numbers)
    for r in range(10):
        
        print(f"{10*r}%...", end='\r')
        for i, n in enumerate(numbers):
            decoder2.shift(i, n)
    
    part1 = decoder.coordinates()
    part2 = decoder2.coordinates()

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

class Node:

    def __init__(self, val, next=None, prev=None):

        self.val = val
        self.next = next
        self.prev = prev

    def __repr__(self):

        return f"{self.val} next={self.next.val} prev={self.prev.val}"

class LinkedList:

    def __init__(self, lst):

            self.length = len(lst)
            self.head = Node((0, lst[0]))

            current = self.head
            for i, number in enumerate(lst[1:], 1):

                current.next = Node((i, number), prev=current)
                current = current.next

                if number == 0:
                    self.zero = (i, number)

            self.head.prev = current
            current.next = self.head

    def shift(self, i, number):

        steps = number % (self.length - 1) if number >= 0 else - (-number % (self.length - 1))
        if steps == 0: return 
        
        current = self.head
        if self.head.val == (i, number):
            self.head = current.next

        else:
            while current.val != (i, number):
                current = current.next

        current.prev.next = current.next
        current.next.prev = current.prev
        
        if number > 0:

            for _ in range(steps):
                current = current.next
            
        else:

            for _ in range(1 - steps):
                current = current.prev

        node = Node((i, number), prev=current, next=current.next)
        current.next.prev = node
        current.next = node

        return node

    def get(self, i, number):

        current = self.head
        while current.next != self.head:
            
            if current.val == (i, number):
                return current
            
            current = current.next

        if current.val == (i, number):
            return current
        
        raise ValueError(f"{number} not in linked list")

    def get_next(self, i, number, offset):

        offset = offset % self.length
        node = self.get(i, number)
        if not offset: return node

        for _ in range(offset):
            node = node.next

        return node 

    def coordinates(self): return sum(self.get_next(*self.zero, offset).val[1] for offset in [1000,2000,3000])
    
    def __iter__(self):

        yield self.head
        current = self.head.next
        while current != self.head:

            yield current
            current = current.next

    def __next__(self):

        n = self.__iter__()
        if n:
            return n

        raise StopIteration


    def to_list(self):

        res = [self.head.val[1]]
        current = self.head.next
        while current != self.head:
            
            res.append(current.val[1])
            current = current.next
        
        return res

    def __repr__(self): return str(self.to_list())

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