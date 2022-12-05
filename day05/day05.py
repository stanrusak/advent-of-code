with open("input.txt", "r") as f:
    data = f.read().strip()

def main():

    crates, instuctions = data.split("\n\n")
    stacks = get_stacks(crates)
    moves = parse_moves(instuctions)

    execute_CrateMover_9000(stacks, moves)
    top_crates = get_top_crates(stacks)
    print(f"Part 1: {top_crates}")

    stacks = get_stacks(crates)
    execute_CrateMover_9001(stacks, moves)
    top_crates = get_top_crates(stacks)
    print(f"Part 2: {top_crates}")

def get_stacks(crates):

    lines = crates.splitlines()
    stack_num = len(lines[-1].strip().split())
    
    stacks = [Stack() for i in range(stack_num)]
    for line in lines[-2::-1]:
        for i in range(1, stack_num+1):
            item =line[i + (i-1)*3]
            if item != ' ':
                stacks[i-1].push(item)
    
    return stacks

def parse_moves(instructions):
    
    moves = []
    for line in instructions.splitlines():
        moves.append([int(i) for i in line.split()[1::2]])
    
    return moves

def execute_CrateMover_9000(stacks, moves):

    for repeat, fr, to in moves:
        for _ in range(repeat):
            ind1 = fr-1
            ind2 = to-1
            item = stacks[ind1].pop()
            stacks[ind2].push(item)
            print(f"Moving item {item} from stack {fr} to stack {to}")

def execute_CrateMover_9001(stacks, moves):

    for item_num, fr, to in moves:
        ind1 = fr-1
        ind2 = to-1
        items = stacks[ind1].pop_multiple(item_num)
        stacks[ind2].push_multiple(items)
        print(f"Moving {item_num} items from stack {fr} to stack {to}")
            
def get_top_crates(stacks):

    result = ""
    for stack in stacks:
        result += stack.peek()
    
    return result

        
class Stack(list):

    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]

    def push_multiple(self, items):
        self.extend(items)
    
    def pop_multiple(self, items):

        result = []
        for i in range(items):
            result.append(self.pop())
        return reversed(result)

if __name__ == "__main__":
    main()