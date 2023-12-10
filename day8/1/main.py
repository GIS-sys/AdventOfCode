from functools import cmp_to_key

class Map:
    def __init__(self):
        self.nodes = {}

    def add(self, line):
        data = line.split(" ")
        nodeFrom = data[0]
        nodeLeft = data[2][1:-1]
        nodeRight = data[3][:-2]
        self.nodes[nodeFrom] = (nodeLeft, nodeRight)

    def start(self, nodeFrom):
        self.currentNode = nodeFrom

    def current(self):
        return self.currentNode

    def next(self, instruction):
        self.currentNode = self.nodes[self.currentNode][0 if instruction == "L" else 1]

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        m = Map()
        for step, line in enumerate(fin):
            if step == 0:
                instructions = line[:-1]
                continue
            if line.strip() == "":
                continue
            m.add(line)
        i = 0
        m.start("AAA")
        while m.current() != "ZZZ":
            m.next(instructions[i])
            i = (i + 1) % len(instructions)
            s += 1
        fout.write(str(s))
