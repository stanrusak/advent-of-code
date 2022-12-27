import pytest, re
from itertools import cycle, zip_longest

with open("input.txt", "r") as f:
    data = f.read()

def main(data):
    
    parsed_data = parse(data)    

    part1 = make_traverse(*parsed_data)
    part2 = make_traverse(*parsed_data, cube=True)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    return part1, part2

def make_traverse(rows, cols, steps, turns, dimensions, cube=False):

    traverser = Traverser(rows, cols, dimensions)
    movement_pattern = traverser.move_on_cube if cube else traverser.move

    for s, turn in list(zip_longest(steps, turns)):

        movement_pattern(s)
        traverser.turn(turn)

    r, c = traverser.current_pos
    d = traverser.current_dir
        
    return 1000 * (r + 1) + 4 * (c + 1) + d 
    
def parse(data):

    mapp, route = data.split('\n\n')

    steps = list(map(int,re.findall(r'\d+', route)))
    turns = re.findall(r'[RL]', route)

    mapp = mapp.splitlines()
    maxrow = len(mapp)
    maxcol = max(len(row) for row in mapp)
    
    rows = []
    for r, row in enumerate(mapp):

        traversible = []
        for c, char in enumerate(row):

            if char != ' ':
                traversible.append((r, c, char))
        
        rows.append(traversible)
    
    cols = []
    for c in range(maxcol):

        traversible = []
        for r in range(maxrow):
            
            try:
                char = mapp[r][c]
            except:
                continue
            if char != ' ':
                traversible.append((r, c, char))
        
        cols.append(traversible)

    return rows, cols, steps, turns, (maxrow, maxcol)

class Traverser:

    def __init__(self, rows, cols, dimensions):


        self.map = {"rows": rows, "cols": cols}
        self.current_pos = (rows[0][0][0], rows[0][0][1])

        self.current_dir = 0
        self.dirs = [("rows", 1, '>'), ("cols", 1, 'v'), ("rows", -1, '<'), ("cols", -1, '^')]
        self.path = {self.current_pos: '>'}
        self.rowmax, self.colmax = dimensions

    def move(self, steps):

        r, c = self.current_pos
        traversable, d, arrow = self.dirs[self.current_dir]
        traversable = self.map["rows"][r] if traversable == "rows" else self.map["cols"][c]

        for i, point in enumerate(traversable):
            if tuple(point[:2]) == (r, c):
                break

        for s in range(steps):

            i += d
            if i == len(traversable):
                i = 0

            if i == -1:
                i = len(traversable) - 1
            
            r, c, char = traversable[i]
            if char == '#':
                return
            
            elif char == '.':
                
                self.path[(r, c)] = arrow

            elif char in ["<>v^"]:
                
                print("been there done that")
                self.path[(r, c)] = arrow

            else:
                raise AssertionError("Whaat?!!!")

            self.current_pos = (r, c)

    def teleport(self):

        r, c = self.current_pos
        side = self.rowmax // 4
        rows = self.map["rows"]
        cols = self.map["cols"]

        if self.current_dir == 0:

            if r < side:

                r, c, char = rows[3 * side - 1 - (r % side)][-1]
                d, arrow = 2, '<'
            
            elif side <= r < 2 * side:

                r, c, char = rows[side - 1][side + (r % side)]
                d, arrow = 3, '^'
            
            elif 2 * side <= r < 3 * side:

                r, c, char = rows[side - 1 - (r % side)][-1]
                d, arrow = 2, '^'

            elif 3 * side <= r < 4 * side:

                r, c, char = rows[3 * side - 1][side + (r % side)]
                d, arrow = 3, '^'


        elif self.current_dir == 1:
            
            if r == side - 1 and 2 * side <= c < 3 * side:

                r, c, char = rows[side + (c % side)][-1]
                d, arrow = 2, '<'
            
            elif r == 3 * side -1 and side <= c < 2 * side:

                r, c, char = rows[3 * side + (c % side)][-1]
                d, arrow = 2, '<'

            elif r == 4 * side - 1:
                
                r, c, char = rows[0][side + (c % side)]
                d, arrow = 1, 'v'
            

        elif self.current_dir == 2:
            
            if r < side:

                r, c, char = rows[3 * side - 1 - (r % side)][0]
                d, arrow = 0, '>'

            elif side <= r < 2 * side:

                r, c, char = rows[2 * side][r % side]
                d, arrow = 1, 'v'
            
            elif 2 * side <= r < 3 * side:

                r, c, char = rows[side - 1 - (r % side)][0]
                d, arrow = 0, '>'

            elif 3 * side <= r < 4 * side:

                r, c, char = rows[0][r % side]
                d, arrow = 1, 'v'
        
        elif self.current_dir == 3:
            
            if r == 0 and side <= c < 2 * side:
                
                r, c, char = rows[3 * side + (c % side)][0]
                d, arrow = 0, '>'
            
            elif r == 0 and 2 * side <=  c <  3 *  side:
                
                r, c, char = rows[-1][c % side]
                d, arrow = 3, '^'

            elif r == 2 * side and c < side:

                r, c, char = rows[side + (c % side)][0]
                d, arrow = 0, '>'
            

        else: raise AssertionError("unreachable")

        if char == '#':
            return False
        
        else:
            
            self.current_pos = r, c
            self.path[(r, c)] = arrow
            self.current_dir = d
            return True

    def move_on_cube(self, steps):

        r, c = self.current_pos
        traversable, d, arrow = self.dirs[self.current_dir]
        traversable = self.map["rows"][r] if traversable == "rows" else self.map["cols"][c]

        for i, point in enumerate(traversable):
            if tuple(point[:2]) == (r, c):
                break

        for s in range(steps):

            i += d
            if i == len(traversable) or i == -1:
                
                if self.teleport():
                    return self.move_on_cube(steps - 1 - s)
                else:
                    return
            
            r, c, char = traversable[i]
            if char == '#':
                return
            
            elif char == '.':
                
                self.path[(r, c)] = arrow

            elif char in ["<>v^"]:
                
                print("been there done that")
                self.path[(r, c)] = arrow

            else:
                raise AssertionError("Whaat?!!!")

            self.current_pos = (r, c)

    def turn(self, where):

        if not where:
            return

        if where == 'R':
            self.current_dir = (self.current_dir + 1) % len(self.dirs)
        elif where == 'L':
            self.current_dir = 3 if self.current_dir == 0 else self.current_dir - 1
        
        *_, arrow = self.dirs[self.current_dir]
        self.path[self.current_pos] = arrow
    
    def show(self):

        filled = {}
        for row in self.map["rows"]:
            for r, c, char in row:

                filled[(r, c)] = char

        rows = []
        for r in range(self.rowmax):
            
            row = ''
            for c in range(self.colmax):

                if (r, c) in self.path:     
                    row += self.path[(r, c)]

                elif (r, c) in filled:
                    row += filled[(r, c)]

                else:
                    row += ' '
            
            rows.append(row)
        
        print('\n'.join(rows))

if __name__ == "__main__":
    main(data)