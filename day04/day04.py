with open("input.txt", "r") as f:
    data = f.read().strip()
    
def main():

    coutained_count = 0
    overlap_count = 0
    for line in data.splitlines():

        elf1, elf2 = line.split(',')
        elf1, elf2 = elf1.split('-'), elf2.split('-')     

        if check(elf1, elf2, "contain"):
            coutained_count += 1

        if check(elf1, elf2, "overlap"):
            overlap_count += 1

    print(f"Part 1: {coutained_count}")
    print(f"Part 2: {overlap_count}")

def check(elf1, elf2, condition):

    index = {"contain": 1, "overlap": 0}[condition]

    if int(elf1[0]) >= int(elf2[0]) and int(elf1[index]) <= int(elf2[1]):
        return True
         
    elif int(elf2[0]) >= int(elf1[0]) and int(elf2[index]) <= int(elf1[1]):
        return True
    
    return False

if __name__ == "__main__":
    main()