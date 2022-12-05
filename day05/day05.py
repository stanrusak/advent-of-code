with open("input.txt", "r") as f:
    data = f.read().strip()

def main(data):

    crates, instuctions = data.split("\n\n")
    stacks = get_stacks(crates)
    moves = parse_moves(instuctions)

    execute_CrateMover_9000(stacks, moves)
    part1 = get_top_crates(stacks)

    stacks = get_stacks(crates)
    execute_CrateMover_9001(stacks, moves)
    part2 = get_top_crates(stacks)
    
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

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

    print("CrateMover9000:")
    for repeat, fr, to in moves:
        for _ in range(repeat):
            ind1 = fr-1
            ind2 = to-1
            item = stacks[ind1].pop()
            stacks[ind2].push(item)
            print(f"  moving item {item} from stack {fr} to stack {to}")

def execute_CrateMover_9001(stacks, moves):


    print("CrateMover9001:")
    for item_num, fr, to in moves:
        ind1 = fr-1
        ind2 = to-1
        items = stacks[ind1].pop_multiple(item_num)
        stacks[ind2].extend(items)
        print(f"  moving {item_num} items from stack {fr} to stack {to}")
            
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
    
    def pop_multiple(self, items):

        result = self[-items:]
        del self[-items:]
        return result

if __name__ == "__main__":
    main(data)