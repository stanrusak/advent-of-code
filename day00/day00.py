with open("input.txt", "r") as f:
    inp = f.read().strip()
    elves = inp.split("\n\n")

def get_calories(elf):
    return sum([int(num) for num in elf.split('\n')])

calories_list = []
for elf in elves:
    
    calories =  get_calories(elf)
    calories_list.append(calories)

calories_list.sort()

print(f"Top elf has {calories_list[-1]} calories.")
print(f"Top 3 elves have {sum(calories_list[-3:])} calories.")