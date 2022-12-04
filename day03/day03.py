with open("input.txt", "r") as f:
    data = f.read().strip()

def main():
    
    rucksacks = data.splitlines()

    # part 1
    priorities = [priority(find_item(rucksack)) for rucksack in rucksacks]
    print(f"Part 1: {sum(priorities)}")

    # part 2
    priorities2 = [priority(find_badge(*rucksacks[i:i+3])) for i in range(0,len(rucksacks),3)]
    print(f"Part 2: {sum(priorities2)}")

def find_item(rucksack):

    middle = len(rucksack) //2
    compartment1 = set(rucksack[:middle])
    compartment2 = set(rucksack[middle:])
    return (compartment1 & compartment2).pop()

def priority(item):

    if item > 'Z':
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

def find_badge(elf1, elf2, elf3):

    return (set(elf1) & set(elf2) & set(elf3)).pop()

if __name__ == "__main__":
    main()