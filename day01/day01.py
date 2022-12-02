SHAPES = {'X': 1, 'Y': 2, 'Z':3}
OUTCOMES = {
                "AX": 3, "AY": 6, "AZ": 0,
                "BX": 0, "BY": 3, "BZ": 6,
                "CX": 6, "CY": 0, "CZ": 3,
           }

MAP = {
        "AX": "AZ", "AY": "AX", "AZ": "AY",
        "BX": "BX", "BY": "BY", "BZ": "BZ",
        "CX": "CY", "CY": "CZ", "CZ": "CX",
        }

def main():

    with open("input.txt", "r") as f:
        strategy = [item[0] + item[2] for item in f.readlines()]

    # part 1: strategy -> outcomes
    score1 = get_score(strategy)

    # part 2 strategy -> part 1 strategy -> outcomes
    strategy2 = map(lambda x: MAP[x], strategy)
    score2 = get_score(strategy2)

    print(f"Part 1: {score1}")
    print(f"Part 2: {score2}")

def get_score(strategy):
    
    score = 0
    for item in strategy:
        score += OUTCOMES[item] + SHAPES[item[1]]
    
    return score

if __name__ == "__main__":
    main()