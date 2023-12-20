from tqdm import tqdm


class Cell:
    def __init__(self, t):
        self.t = t
        # self.empty = (t == ".")
        # self.splitter = (t in "-|")
        # self.mirror = (t in "/\\")
        self.lights = [False for _ in range(4)] # right, bottom, left, top

    def energize(self, neighbours):
        prev_lights = [x for x in self.lights]
        if neighbours[0].lights[0]:
            if self.t == ".":
                self.lights[0] = True
            if self.t == "-":
                self.lights[0] = True
            if self.t == "|":
                self.lights[1] = True
                self.lights[3] = True
            if self.t == "/":
                self.lights[3] = True
            if self.t == "\\":
                self.lights[1] = True
        if neighbours[2].lights[2]:
            if self.t == ".":
                self.lights[2] = True
            if self.t == "-":
                self.lights[2] = True
            if self.t == "|":
                self.lights[1] = True
                self.lights[3] = True
            if self.t == "/":
                self.lights[1] = True
            if self.t == "\\":
                self.lights[3] = True
        if neighbours[1].lights[1]:
            if self.t == ".":
                self.lights[1] = True
            if self.t == "-":
                self.lights[0] = True
                self.lights[2] = True
            if self.t == "|":
                self.lights[1] = True
            if self.t == "/":
                self.lights[2] = True
            if self.t == "\\":
                self.lights[0] = True
        if neighbours[3].lights[3]:
            if self.t == ".":
                self.lights[3] = True
            if self.t == "-":
                self.lights[0] = True
                self.lights[2] = True
            if self.t == "|":
                self.lights[3] = True
            if self.t == "/":
                self.lights[0] = True
            if self.t == "\\":
                self.lights[2] = True
        return prev_lights != self.lights

    def __repr__(self):
        return self.t + str(int(self.lights[0])) + str(int(self.lights[1])) + str(int(self.lights[2])) + str(int(self.lights[3]))

class Field:
    def __init__(self, lines, starting_point=(0, 0), starting_direction=[0]):
        self.cells = [[Cell(cell) for cell in line] for line in lines]
        self.cells[starting_point[1]][starting_point[0]].lights[starting_direction] = True

    def get_or_default(self, x, y):
        if y >= 0 and y < len(self.cells) and x >= 0 and x < len(self.cells[y]):
            return self.cells[y][x]
        return Cell(".")

    def get_neighbours(self, x, y):
        # left, top, right, bottom
        neighbours = []
        neighbours.append(self.get_or_default(x-1, y))
        neighbours.append(self.get_or_default(x, y-1))
        neighbours.append(self.get_or_default(x+1, y))
        neighbours.append(self.get_or_default(x, y+1))
        return neighbours

    def energize(self):
        changed = True
        while changed:
            changed = False
            for y in range(len(self.cells)):
                for x, c in enumerate(self.cells[y]):
                    changed = c.energize(self.get_neighbours(x, y)) or changed
            # self.print_debug()
            print(self)

    def count_energized(self):
        res = 0
        for r in self.cells:
            for c in r:
                if True in c.lights:
                    res += 1
        return res

    def print_debug(self):
        print("\n".join([" ".join([str(c) for c in r]) for r in self.cells]))
        print("")

    def __repr__(self):
        res = ""
        for r in self.cells:
            for c in r:
                slights = "".join([str(int(x)) for x in c.lights])
                if slights == "0000":
                    res += "."
                elif slights == "0001":
                    res += "\u2191"
                elif slights == "0010":
                    res += "\u2190"
                elif slights == "0100":
                    res += "\u2193"
                elif slights == "1000":
                    res += "\u2192"
                elif slights == "0011":
                    res += "\u2198"
                elif slights == "0101":
                    res += "\u2195"
                elif slights == "1001":
                    res += "\u2199"
                elif slights == "0110":
                    res += "\u2197"
                elif slights == "1010":
                    res += "\u2194"
                elif slights == "1100":
                    res += "\u2196"
                elif slights == "0111":
                    res += "#"
                elif slights == "1011":
                    res += "#"
                elif slights == "1101":
                    res += "#"
                elif slights == "1110":
                    res += "#"
                elif slights == "1111":
                    res += "#"
                else:
                    res += "?"
            res += "\n"
        return res

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        lines = []
        for line in fin:
            line = line.strip()
            if line == "":
                break
            lines.append(line)
        all_sides = [] # coordinates + direction (left, top, right, bottom)
        all_sides += [((0, i), 0) for i in range(len(lines))]
        all_sides += [((i, 0), 1) for i in range(len(lines[0]))]
        all_sides += [((len(lines[0])-1, i), 2) for i in range(len(lines))]
        all_sides += [((i, len(lines)-1), 3) for i in range(len(lines[0]))]
        for starting in tqdm(all_sides):
            field = Field(lines, starting_point=starting[0], starting_direction=starting[1])
            field.energize()
            energy = field.count_energized()
            s = max(s, energy)
            with open(f"tmp/{energy}_{starting[0][0]}_{starting[0][1]}_{starting[1]}.txt", "w") as ftmp:
                ftmp.write(str(field))
        fout.write(str(s))

